from exceptions import ApiError
from models import Project, ProjectUserRole, UserPosition, ProjectCalendarPlan, \
    ProjectCalendarPlanUserRole, User, ProjectCalendarPlanRole


def get_resource_working(project_id: int):
    projects = Project.fetch(Project.id == project_id)[0]
    if not projects:
        raise ApiError.BadRequest('Project not found')

    data = []

    workers = ProjectUserRole.select().where(ProjectUserRole.project == project_id)
    grouped_workers = ProjectUserRole.select().where(ProjectUserRole.project == project_id).group_by(ProjectUserRole.user)

    for worker in grouped_workers:
        fullname = f'{worker.user.firstname} {worker.user.lastname} {worker.user.surname}'

        position = UserPosition.get(UserPosition.user == worker.user.id).position

        roles = []
        for more_worker in workers:
            if worker.user.id == more_worker.user.id:
                roles.append({
                'name': more_worker.role.name,
                'description': more_worker.role.description
            })

        data.append({
            'key': worker.id,
            'fullname': fullname,
            'position': position.name,
            'departament': position.department.name,
            'roles': roles
        })

    return data


def get_resource_cp(project_id: int):
    projects = Project.fetch(Project.id == project_id)[0]
    if not projects:
        raise ApiError.BadRequest('Project not found')

    data = []

    workers = (ProjectCalendarPlanUserRole
               .select(ProjectCalendarPlanUserRole, User, ProjectCalendarPlanRole, ProjectCalendarPlan)
               .join(ProjectCalendarPlan)
               .join_from(ProjectCalendarPlanUserRole, User)
               .join_from(ProjectCalendarPlanUserRole, ProjectCalendarPlanRole)
               .where(ProjectCalendarPlan.project == project_id))

    for worker in workers:
        fullname = f'{worker.user.firstname} {worker.user.lastname} {worker.user.surname}'
        role_name = worker.role.name
        task_name = worker.calendar_plan.name

        start_date_fact = worker.calendar_plan.start_date_fact.strftime('%d.%m.%Y') \
            if worker.calendar_plan.start_date_fact else ''
        end_date_fact = worker.calendar_plan.end_date_fact.strftime('%d.%m.%Y') \
            if worker.calendar_plan.end_date_fact else ''
        end_date_forecast = worker.calendar_plan.end_date_forecast.strftime('%d.%m.%Y') \
            if worker.calendar_plan.end_date_forecast else ''
        start_date_forecast = worker.calendar_plan.start_date_forecast.strftime('%d.%m.%Y') \
            if worker.calendar_plan.start_date_forecast else ''

        if start_date_fact and end_date_fact:
            dates = f'{start_date_fact} - {end_date_fact}'
        elif start_date_fact:
            dates = f'{start_date_fact} - {end_date_forecast}'
        elif end_date_fact:
            dates = f'{start_date_forecast} - {end_date_fact}'
        else:
            dates = f'{start_date_forecast} - {end_date_forecast}'

        data.append({
            'key': worker.id,
            'fullname': fullname,
            'role_name': role_name,
            'task': task_name,
            'dates': dates
        })

    return data
