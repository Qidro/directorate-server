from datetime import date
from models import Project, User, ProjectResults, ProjectResultsRoles, ProjectResultsUserRole, ProjectResultValues
from constants.constants import project_result_status_list
from exceptions import ApiError


def create_result(
        project_id: int, name: str, type: str,
        units_measure: str, characteristic: str, approval_doc: str
):
    project = Project.fetch(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    result = ProjectResults(
        project=project_id,
        name=name,
        type=type,
        units_measure=units_measure,
        characteristic=characteristic,
        approval_doc=approval_doc,
        status='IN_PROGRESS'
    )
    result.save()

    return result.get_dto()


def edit_result(
        result_id: int, name: str, type: str,
        units_measure: str, characteristic: str, approval_doc: str,  status: str
):
    project_result = ProjectResults.get_or_none(ProjectResults.id == result_id)
    if not project_result:
        raise ApiError.BadRequest('Project result not found')

    if status not in project_result_status_list:
        ApiError.BadRequest('Status not found')

    prev_result_data = ProjectResults.fetch(ProjectResults.id == result_id)[0].get_dto()

    project_result.name = name
    project_result.type = type
    project_result.units_measure = units_measure
    project_result.characteristic = characteristic
    project_result.approval_doc = approval_doc
    project_result.status = status
    project_result.save()

    new_result_data = ProjectResults.fetch(ProjectResults.id == result_id)[0].get_dto()

    return new_result_data, prev_result_data


def remove_result(result_id: int):
    try:
        result = ProjectResults.fetch(ProjectResults.id == result_id)[0]
    except IndexError:
        return

    ProjectResults.delete().where(ProjectResults.id == result_id).execute()
    return result.get_dto()


def get_all_results():
    return [project_result.get_dto() for project_result in ProjectResults.fetch()]


def result_set_user_role(user_id: int, role_id: int, project_result_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectResultsRoles.get_or_none(ProjectResultsRoles.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    project_result = ProjectResults.get_or_none(ProjectResults.id == project_result_id)
    if not project_result:
        raise ApiError.BadRequest('Project result not found')

    user_role = ProjectResultsUserRole.get_or_none(user=user, role=role, project_result=project_result)
    if user_role:
        raise ApiError.BadRequest('User has already been assigned to this role')

    project_result_user_role = ProjectResultsUserRole(user=user, role=role, project_result=project_result)
    project_result_user_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def remove_result_role(user_id: int, role_id: int, project_result_id: int):
    project_result = ProjectResults.get_or_none(ProjectResults.id == project_result_id)
    if not project_result:
        raise ApiError.BadRequest('Project result not found')

    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectResultsRoles.get_or_none(ProjectResultsRoles.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    user_role = ProjectResultsUserRole.get_or_none(user=user, role=role, project_result=project_result)
    if not user_role:
        raise ApiError.BadRequest('User is not assigned to this role')

    ProjectResultsUserRole.delete().where(ProjectResultsUserRole.id == user_role).execute()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def get_roles():
    roles = ProjectResultsRoles.select()
    return [role.get_dto() for role in roles]


def get_one_result(result_id: int):
    project_result = ProjectResults.fetch(ProjectResults.id == result_id)
    if len(project_result) == 0:
        raise ApiError.BadRequest('Project result not found')

    return project_result[0].get_dto()


def get_project_results(project_id: int):
    project_results = ProjectResults.fetch(ProjectResults.project == project_id)
    return [project_result.get_dto() for project_result in project_results]


def create_result_value(result_id: int, achievement_date: date, plan: int, forecast: int):
    project = ProjectResults.select().where(ProjectResults.id == result_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    project = [data.get_dto() for data in project][0]

    result_meaning = ProjectResultValues(
        result=result_id,
        achievement_date=achievement_date,
        units_measure=project['units_measure'],
        plan=plan,
        forecast=forecast
    )
    result_meaning.save()

    return result_meaning.get_dto()


def update_result_value(value_id: int, achievement_date: date, plan: int, forecast: int):
    value = ProjectResultValues.get_or_none(ProjectResultValues.id == value_id)
    if not value:
        raise ApiError.BadRequest('Value not found')

    prev_value_data = value.get_dto()

    value.achievement_date = achievement_date
    value.plan = plan
    value.forecast = forecast
    value.save()

    new_value_data = value.get_dto()

    return new_value_data, prev_value_data


def remove_result_value(value_id: int):
    value = ProjectResultValues.get_or_none(ProjectResultValues.id == value_id)
    if not value:
        return

    ProjectResultValues.delete().where(ProjectResultValues.id == value_id).execute()
    return value.get_dto()


def get_result_values(result_id: int):
    result = ProjectResults.get_or_none(id=result_id)
    if not result:
        raise ApiError.BadRequest('Result not found')

    result_values = ProjectResultValues.select().where(ProjectResultValues.result == result)
    return [value.get_dto() for value in result_values]
