from werkzeug.datastructures import FileStorage
from datetime import date
from models import Backpack, User, BackpackUserRole, BackpackRole, Project,\
    ProjectIndicators, ProjectIndicatorsValues, ProjectContracts, BackpackDocument, \
    ProjectCalendarPlan, ProjectBudget
from exceptions import ApiError
from service import file_service, project_calendar_plan_service, project_budget_service


def create(name: str, description: str):
    backpack = Backpack(
        name=name,
        description=description,
    )
    backpack.save()

    return Backpack.fetch(Backpack.id == backpack.id)[0].get_dto()


def get(backpack_id: int):
    backpack = Backpack.fetch(Backpack.id == backpack_id)
    if len(backpack) == 0:
        raise ApiError.BadRequest('Backpack not found')

    return backpack[0].get_dto()


def add_user_role(user_id: int, role_id: int, backpack_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = BackpackRole.get_or_none(BackpackRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    backpack_users_role = BackpackUserRole(user=user, role=role, backpack=backpack)
    backpack_users_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def remove_user_role(user_id: int, role_id: int, backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Project result not found')

    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = BackpackRole.get_or_none(BackpackRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    user_role = BackpackUserRole.get_or_none(user=user, role=role, backpack=backpack)
    if not user_role:
        raise ApiError.BadRequest('User is not assigned to this role')

    BackpackUserRole.delete().where(BackpackUserRole.id == user_role).execute()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def update(backpack_id: int, name: str, description: str):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    prev_backpack_data = Backpack.fetch(Backpack.id == backpack_id)[0].get_dto()

    backpack.name = name
    backpack.description = description
    backpack.change_date = date.today()
    backpack.save()

    new_backpack_data = Backpack.fetch(Backpack.id == backpack_id)[0].get_dto()

    return new_backpack_data, prev_backpack_data


def delete(backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    backpack.is_Archived = True
    backpack.change_date = date.today()
    backpack.save()


def get_all():
    backpacks = Backpack.fetch(Backpack.is_Archived == False)
    return [backpack.get_dto() for backpack in backpacks]


def get_my(user):
    backpacks = Backpack.fetch(BackpackUserRole.user == user.id)
    return [backpack.get_dto() for backpack in backpacks if not backpack.is_Archived]


def get_roles():
    roles = BackpackRole.select()
    return [role.get_dto() for role in roles]


def get_indicators(backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    projects = Project.fetch(Project.backpack == backpack_id)

    result = []
    indicators_value = []
    for project in projects:
        project_indicators = [
            indicator.get_dto() for indicator in
            ProjectIndicators.fetch(ProjectIndicators.project == project.id)
        ]
        result.append({
            'id': project.id,
            'name': project.name,
            'status': project.status,
            'indicators': project_indicators
        })

        project_indicators_value = [
            value.get_dto() for value in ProjectIndicatorsValues.select().join(ProjectIndicators)
            .where(
                ProjectIndicators.project == project.id,
                ProjectIndicatorsValues.period.month == date.today().month,
                ProjectIndicatorsValues.period.year == date.today().year
            )
        ]
        indicators_value.extend(project_indicators_value)

    new_result = []
    for group in result:
        new_indicators = []
        for indicator in group['indicators']:
            indicator['status'] = 'AWAITING'
            for value in indicators_value:
                if value['indicator']['id'] == indicator['id']:
                    indicator['actual_value'] = value['actual_value']
                    indicator['forecast_value'] = value['forecast_value']
                    indicator['plan_value'] = value['plan_value']
                    indicator['status'] = value['status']
            new_indicators.append(indicator)
        new_result.append({
            'id': group['id'],
            'name': group['name'],
            'status': group['status'],
            'indicators': new_indicators
        })
    return new_result


def get_calendar_plans(backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    projects = Project.fetch(Project.backpack == backpack_id)

    result = []
    for project in projects:
        project_calendar_plans = project_calendar_plan_service.get_calendar_plans(project.id)

        result.append({
            'id': project.id,
            'name': project.name,
            'status': project.status,
            'calendar_plans': project_calendar_plans
        })

    return result


def get_contracts(backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    projects = Project.fetch(Project.backpack == backpack_id)

    result = []
    for project in projects:
        project_contracts = ProjectContracts.fetch(ProjectContracts.project == project.id)
        result.append({
            'id': project.id,
            'name': project.name,
            'contracts': [contract.get_dto() for contract in project_contracts]
        })

    return result


def get_budgets(backpack_id: int):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    projects = Project.fetch(Project.backpack == backpack_id)

    result = []
    for project in projects:
        budgets = project_budget_service.get_budgets(project.id)
        result.append({
            'id': project.id,
            'name': project.name,
            'status': project.status,
            'budgets': budgets
        })

    return result


def save_backpack_file(file: FileStorage, backpack_id: int, file_type: str):
    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    file = file_service.save_file(file)

    document = BackpackDocument(
        backpack=backpack,
        file=file,
        type=file_type
    )
    document.save()

    return document.get_dto()


def remove_file(file_id: str, backpack_id: int):
    document = BackpackDocument.get_or_none(backpack=backpack_id, file=file_id)
    if not document:
        raise ApiError.BadRequest('File not found')

    BackpackDocument.delete().where(BackpackDocument.id == document).execute()

    return document.get_dto()
