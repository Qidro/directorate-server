import datetime

from exceptions import ApiError
from models import Project, ProjectResults, ProjectCalendarPlan, ProjectCalendarPlanCP, ProjectCalendarPlanResults, \
                ProjectCalendarPlanRole, ProjectCalendarPlanUserRole, User


def calc_days(start_date, end_date):
    length_of_days = (end_date - start_date).days

    dates = [start_date + datetime.timedelta(idx + 1)
             for idx in range((end_date - start_date).days)]

    working_days = sum(1 for day in dates if day.weekday() < 5)

    return length_of_days, working_days


def get_days(type: str, start_date_fact: datetime.date, end_date_fact: datetime.date, start_date_plan: datetime.date,
             end_date_plan: datetime.date):
    length_of_days, working_days = None, None

    if type in ['WORK', 'STAGE']:
        if start_date_fact:
            if end_date_fact:
                length_of_days, working_days = calc_days(start_date_fact, end_date_fact)
            else:
                length_of_days, working_days = calc_days(start_date_fact, end_date_plan)
        elif start_date_plan:
            if end_date_fact:
                length_of_days, working_days = calc_days(start_date_plan, end_date_fact)
            else:
                length_of_days, working_days = calc_days(start_date_plan, end_date_plan)

    return length_of_days, working_days


def get_status(end_date_plan: datetime.date, end_date_forecast: datetime.date):
    if end_date_forecast and end_date_forecast < datetime.date.today():
        status = 'OVERDUE'
    elif end_date_forecast and end_date_plan and end_date_plan != end_date_forecast:
        status = 'FORECAST_FAILURE'
    else:
        status = 'IN_WORK'

    return status


def update_parent_stage(parent_stage_id: int, children_work_id: int):
    parent_stage = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == parent_stage_id)[0]
    children_work = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == children_work_id)[0]
    if children_work.status in ['IN_WORK', 'OVERDUE']:
        parent_stage.status = children_work.status

    if children_work.start_date_plan < parent_stage.start_date_plan:
        parent_stage.start_date_plan = children_work.start_date_plan

    if children_work.end_date_plan > parent_stage.end_date_plan:
        parent_stage.end_date_plan = children_work.end_date_plan

    if not parent_stage.start_date_forecast:
        parent_stage.start_date_forecast = children_work.start_date_forecast
    elif children_work.start_date_forecast and children_work.start_date_forecast < parent_stage.start_date_forecast:
        parent_stage.start_date_forecast = children_work.start_date_forecast

    if not parent_stage.end_date_forecast:
        parent_stage.end_date_forecast = children_work.end_date_forecast
    elif children_work.end_date_forecast and children_work.end_date_forecast > parent_stage.end_date_forecast:
        parent_stage.end_date_forecast = children_work.end_date_forecast

    if not parent_stage.start_date_fact:
        parent_stage.start_date_fact = children_work.start_date_fact
    elif children_work.start_date_fact and children_work.start_date_fact < parent_stage.start_date_fact:
        parent_stage.start_date_fact = children_work.start_date_fact

    if not parent_stage.end_date_fact:
        parent_stage.end_date_fact = children_work.end_date_fact
    elif children_work.end_date_fact and children_work.end_date_fact > parent_stage.end_date_fact:
        parent_stage.end_date_fact = children_work.end_date_fact

    length_of_days, working_days = get_days(parent_stage.type, parent_stage.start_date_fact, parent_stage.end_date_fact,
                                            parent_stage.start_date_plan, parent_stage.end_date_plan)

    parent_stage.length_of_days = length_of_days
    parent_stage.working_days = working_days

    parent_stage.save()

    return


def create_stage(project_id: int, type: str, name: str, awaiting_result: str):
    project = Project.get_or_none(id=project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    date = datetime.date.today()

    project_calendar_plan = ProjectCalendarPlan(
        project=project,
        type=type,
        name=name,
        awaiting_result=awaiting_result,
        start_date_plan=date,
        length_of_days=1,
        working_days=1,
        end_date_plan=date,
        status='IN_WORK'
    )
    project_calendar_plan.save()

    return ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == project_calendar_plan)[0].get_dto()


def update_stage(calendar_plan_id: int, name: str, awaiting_result: str):
    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    prev_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    project_calendar_plan.awaiting_result = awaiting_result
    project_calendar_plan.name = name
    project_calendar_plan.save()

    new_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    children_calendar_plans = ProjectCalendarPlan.fetch(ProjectCalendarPlan.parent_stage_id == project_calendar_plan.id)
    children = [children_calendar_plan.get_dto() for children_calendar_plan in children_calendar_plans]

    return {**new_cp_data, 'children': children}, {**prev_cp_data, 'children': children}


def create_work(project_id: int, type: str, name: str, awaiting_result: str, start_date_plan: datetime.date,
                start_date_forecast: datetime.date, start_date_fact: datetime.date, end_date_plan: datetime.date,
                end_date_forecast: datetime.date, end_date_fact: datetime.date, executor_id: int, approval_doc: str,
                parent_stage_id: int):

    project = Project.get_or_none(id=project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    length_of_days, working_days = get_days(type, start_date_fact, end_date_fact, start_date_plan, end_date_plan)

    parent_stage = ProjectCalendarPlan.get_or_none(id=parent_stage_id)
    if not parent_stage:
        raise ApiError.BadRequest('Parent stage not found')

    status = get_status(end_date_plan, end_date_forecast)

    project_calendar_plan = ProjectCalendarPlan(
        project=project,
        type=type,
        name=name,
        awaiting_result=awaiting_result,
        start_date_plan=start_date_plan,
        start_date_forecast=start_date_forecast,
        start_date_fact=start_date_fact,
        length_of_days=length_of_days,
        working_days=working_days,
        end_date_plan=end_date_plan,
        end_date_forecast=end_date_forecast,
        end_date_fact=end_date_fact,
        approval_doc=approval_doc,
        status=status,
        parent_stage_id=parent_stage_id
    )
    project_calendar_plan.save()

    executor_role_id = ProjectCalendarPlanRole.get_or_none(slug='EXECUTOR')

    set_user_role(executor_id, project_calendar_plan, executor_role_id)

    update_parent_stage(parent_stage_id, project_calendar_plan.id)

    return ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == project_calendar_plan)[0].get_dto()


def create_point(project_id: int, type: str, name: str, end_date_plan: datetime.date, end_date_forecast: datetime.date,
           end_date_fact: datetime.date, executor_id: int, approval_doc: str):

    project = Project.get_or_none(id=project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    status = get_status(end_date_plan, end_date_forecast)

    project_calendar_plan = ProjectCalendarPlan(
        project=project,
        type=type,
        name=name,
        end_date_plan=end_date_plan,
        end_date_forecast=end_date_forecast,
        end_date_fact=end_date_fact,
        approval_doc=approval_doc,
        status=status
    )
    project_calendar_plan.save()

    if type == 'INITIATION':
        project.start_date = end_date_fact

    if type == 'COMPLETION':
        project.end_date = end_date_fact

    project.save()

    executor_role_id = ProjectCalendarPlanRole.get_or_none(slug='EXECUTOR')

    set_user_role(executor_id, project_calendar_plan, executor_role_id)

    return ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == project_calendar_plan)[0].get_dto()


def update_work(calendar_plan_id: int, type: str, name: str, awaiting_result: str, start_date_plan: datetime.date,
           start_date_forecast: datetime.date, start_date_fact: datetime.date, end_date_plan: datetime.date,
           end_date_forecast: datetime.date, end_date_fact: datetime.date, approval_doc: str, parent_stage_id: int):

    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    length_of_days, working_days = get_days(type, start_date_fact, end_date_fact, start_date_plan, end_date_plan)

    prev_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    status = get_status(end_date_plan, end_date_forecast)

    project_calendar_plan.name = name
    project_calendar_plan.awaiting_result = awaiting_result
    project_calendar_plan.start_date_plan = start_date_plan
    project_calendar_plan.start_date_forecast = start_date_forecast
    project_calendar_plan.start_date_fact = start_date_fact
    project_calendar_plan.length_of_days = length_of_days
    project_calendar_plan.working_days = working_days
    project_calendar_plan.end_date_plan = end_date_plan
    project_calendar_plan.end_date_forecast = end_date_forecast
    project_calendar_plan.end_date_fact = end_date_fact
    project_calendar_plan.approval_doc = approval_doc
    project_calendar_plan.status = status
    project_calendar_plan.save()

    update_parent_stage(parent_stage_id, project_calendar_plan.id)

    new_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    return new_cp_data, prev_cp_data


def update_point(calendar_plan_id: int, name: str, end_date_plan: datetime.date,
                 end_date_forecast: datetime.date, end_date_fact: datetime.date, approval_doc: str):

    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    prev_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    status = get_status(end_date_plan, end_date_forecast)

    project_calendar_plan.name = name
    project_calendar_plan.end_date_plan = end_date_plan
    project_calendar_plan.end_date_forecast = end_date_forecast
    project_calendar_plan.end_date_fact = end_date_fact
    project_calendar_plan.approval_doc = approval_doc
    project_calendar_plan.status = status
    project_calendar_plan.save()

    new_cp_data = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

    return new_cp_data, prev_cp_data


def delete(calendar_plan_id):
    project_calendar_plan = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0]
    if project_calendar_plan.type == 'STAGE':
        ProjectCalendarPlan.delete().where(ProjectCalendarPlan.parent_stage_id == calendar_plan_id).execute()

    ProjectCalendarPlan.delete().where(ProjectCalendarPlan.id == calendar_plan_id).execute()
    return


def get_stages(project_id: int):
    project_calendar_plans = (
        ProjectCalendarPlan
        .select(ProjectCalendarPlan, Project)
        .left_outer_join(Project, on=(Project.id == ProjectCalendarPlan.project))
        .where(ProjectCalendarPlan.project == project_id, ProjectCalendarPlan.type == 'STAGE')
    )

    project_calendar_plan_stages = [project_calendar_plan.get_dto() for project_calendar_plan in project_calendar_plans]
    return project_calendar_plan_stages


def get_calendar_plans(project_id: int):
    project_calendar_plans = ProjectCalendarPlan.fetch(
        condition=((ProjectCalendarPlan.project == project_id) & (ProjectCalendarPlan.parent_stage_id == None))
    )

    project_calendar_plans_new = []

    for project_calendar_plan in project_calendar_plans:
        if project_calendar_plan.type != 'STAGE':
            if not project_calendar_plan.end_date_fact and project_calendar_plan.end_date_forecast < datetime.date.today():
                project_calendar_plan.status = 'OVERDUE'
                project_calendar_plan.save()

            complete_point_count = 0
            calendar_plan_results = ProjectCalendarPlanResults.fetch(
                ProjectCalendarPlanResults.calendar_plan == project_calendar_plan)
            for result in calendar_plan_results:
                if result.result.status in ['COMPLETED', 'ACHIEVED']:
                    complete_point_count += 1

            if complete_point_count != 0 and complete_point_count == len(
                    calendar_plan_results) and project_calendar_plan.status != 'CONFIRMED':
                project_calendar_plan.status = 'COMPLETE'
                project_calendar_plan.save()

            project_calendar_plan = project_calendar_plan.get_dto()
        else:
            children_calendar_plans = ProjectCalendarPlan.fetch(
                ProjectCalendarPlan.parent_stage_id == project_calendar_plan.id)

            complete_work_count = 0
            for children_calendar_plan in children_calendar_plans:
                if children_calendar_plan.status == 'OVERDUE':
                    project_calendar_plan.status = children_calendar_plan.status

                if children_calendar_plan.status in ['COMPLETE', 'CONFIRMED']:
                    complete_work_count += 1

            if complete_work_count != 0 and complete_work_count == len(children_calendar_plans):
                project_calendar_plan.status = 'COMPLETE'

            project_calendar_plan.save()

            project_calendar_plan = project_calendar_plan.get_dto()

            project_calendar_plan['children'] = [children_calendar_plan.get_dto()
                                                 for children_calendar_plan in children_calendar_plans]

        project_calendar_plans_new.append(project_calendar_plan)

    return project_calendar_plans_new


def get_calendar_plan(calendar_plan_id: int):
    project_calendar_plan = ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)
    if len(project_calendar_plan) == 0:
        raise ApiError.BadRequest('Calendar plan not found')

    results = [result.get_dto() for result in
               ProjectCalendarPlanResults.fetch(ProjectCalendarPlanResults.calendar_plan == project_calendar_plan)
               ]

    project_calendar_plan = project_calendar_plan[0]

    if project_calendar_plan.type == 'STAGE':
        children_calendar_plans = ProjectCalendarPlan.fetch(
                ProjectCalendarPlan.parent_stage_id == project_calendar_plan.id)
        return {
            **project_calendar_plan.get_dto(),
            'children': [children_calendar_plan.get_dto()
                         for children_calendar_plan in children_calendar_plans]
        }
    else:
        return {
            **project_calendar_plan.get_dto(),
            'results': results
        }


def add_result(calendar_plan_id: int, result_id: int):
    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    project_result = ProjectResults.get_or_none(id=result_id)
    if not project_result:
        raise ApiError.BadRequest('Result not found')

    calendar_plan_result = ProjectCalendarPlanResults(calendar_plan=project_calendar_plan, result=project_result)
    calendar_plan_result.save()

    complete_point_count = 0
    calendar_plan_results = ProjectCalendarPlanResults.fetch(ProjectCalendarPlanResults.calendar_plan == project_calendar_plan)
    for result in calendar_plan_results:
        if result.result.status in ['COMPLETED', 'ACHIEVED']:
            complete_point_count += 1

    if complete_point_count != 0 and complete_point_count == len(calendar_plan_results):
        project_calendar_plan.status = 'COMPLETE'
        project_calendar_plan.save()

    return calendar_plan_result.get_dto()


def remove_result(calendar_plan_id: int, result_id: int):
    result = ProjectCalendarPlanResults.get_or_none(ProjectCalendarPlanResults.calendar_plan == calendar_plan_id, ProjectCalendarPlanResults.result == result_id)
    if not result:
        return

    ProjectCalendarPlanResults.delete().where(ProjectCalendarPlanResults.id == result).execute()

    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)

    complete_point_count = 0
    calendar_plan_results = ProjectCalendarPlanResults.fetch(
        ProjectCalendarPlanResults.calendar_plan == project_calendar_plan)
    for result in calendar_plan_results:
        if result.result.status in ['COMPLETED', 'ACHIEVED']:
            complete_point_count += 1

    if complete_point_count != 0 and complete_point_count == len(calendar_plan_results):
        project_calendar_plan.status = 'COMPLETE'
    else:
        project_calendar_plan.status = 'IN_WORK'

    project_calendar_plan.save()

    return result.get_dto()


def get_cp():
    return [project_calendar_plan_cp.get_dto() for project_calendar_plan_cp in ProjectCalendarPlanCP.select()]


def get_roles():
    return [project_calendar_plan_roles.get_dto() for project_calendar_plan_roles in ProjectCalendarPlanRole.select()]


def set_user_role(user_id: int, calendar_plan_id: int, role_id: int):
    user = User.get_or_none(id=user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    role = ProjectCalendarPlanRole.get_or_none(id=role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    user_role = ProjectCalendarPlanUserRole(
        user=user,
        role=role,
        calendar_plan=project_calendar_plan
    )
    user_role.save()

    return {
        'id': user.id,
        'fullname':  f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def remove_user_role(user_id: int, calendar_plan_id: int, role_id: int):
    user = User.get_or_none(id=user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    role = ProjectCalendarPlanRole.get_or_none(id=role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    user_role = ProjectCalendarPlanUserRole.get_or_none(user=user, role=role, calendar_plan=project_calendar_plan)
    if not user_role:
        raise ApiError.BadRequest('User is not assigned to this role')

    ProjectCalendarPlanUserRole.delete().where(ProjectCalendarPlanUserRole.id == user_role).execute()
    return {
        'id': user.id,
        'fullname':  f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def update_status(calendar_plan_id: int, status: str):
    project_calendar_plan = ProjectCalendarPlan.get_or_none(id=calendar_plan_id)
    if not project_calendar_plan:
        raise ApiError.BadRequest('Calendar plan not found')

    project_calendar_plan.status = status
    project_calendar_plan.save()

    return ProjectCalendarPlan.fetch(ProjectCalendarPlan.id == calendar_plan_id)[0].get_dto()

