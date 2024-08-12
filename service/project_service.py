from datetime import date
from werkzeug.datastructures import FileStorage
from models import Project, User, ProjectUserRole, ProjectRole, ProjectIndicators, ProjectIndicatorsRole, \
    ProjectIndicatorsUserRole, Proposal, Backpack, ProjectIndicatorsValues, ProjectDocument
from exceptions import ApiError
from constants.constants import project_status_list, project_priority_list, \
    indicator_evaluation_list, coverage_list, indicator_status_list
import datetime

from service import file_service
from .log import project_log_service


def get_project(user, project_id: int):
    project = Project.fetch(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    documents = ProjectDocument.fetch(ProjectDocument.project == project)
    documents = [doc.get_dto() for doc in documents]

    return {**project[0].get_dto(), 'documents': documents}


def create(proposal_id: int, backpack_id: int, user_id: int, user_curator_id: int):
    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    curator = User.get_or_none(User.id == user_curator_id)
    if not curator:
        raise ApiError.BadRequest('User not found')

    backpack = Backpack.get_or_none(Backpack.id == backpack_id)
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    if proposal.status != 'SUCCESS':
        raise ApiError.BadRequest('Proposal no status success')

    project = Project(
        backpack=backpack,
        name=proposal.name,
        short_name="",
        priority='NORMAL',
        type="",
        start_date=None,
        end_date=None,
        description="",
        formal_basis="",
        project_justification=proposal.justification,
        additional_info="",
        project_goals=proposal.purpose,
        status='INITIATION',
        proposal_id=proposal_id
    )
    project.save()
    user_supervisor = ProjectUserRole(
        user=user,
        role=3,
        project=project.id
    )
    user_supervisor.save()

    user_curator = ProjectUserRole(
        user=curator,
        role=9,
        project=project.id
    )
    user_curator.save()

    proposal.isArchived = True
    proposal.status = 'ARCHIVED'
    proposal.save()

    documents = ProjectDocument.fetch(ProjectDocument.project == project)
    documents = [doc.get_dto() for doc in documents]

    return {**project.get_dto(), 'documents': documents}


def update_stage(project_id: int, status: str, user_id: int):
    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    if status not in project_status_list:
        ApiError.BadRequest('Status not found')

    project.status = status

    project.save()

    documents = ProjectDocument.fetch(ProjectDocument.project == project)
    documents = [doc.get_dto() for doc in documents]

    return {**project.get_dto(), 'documents': documents}


def get_projects():
    projects = Project.fetch(Project.is_Archived == False)
    return [project.get_dto() for project in projects]


def delete(project_id: int):
    project = Project.get_or_none(Project.id == project_id)
    project.is_Archived = True
    project.save()


def update(
        project_id: int, name: str, short_name: str, priority: str,
        type: str, description: str, formal_basis: str, project_justification: str,
        additional_info: str, project_goals: str, risks: str, deviations: str):
    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    if priority not in project_priority_list:
        raise ApiError.BadRequest('Project has no such priority')

    prev_project_data = Project.fetch(Project.id == project_id)[0].get_dto()

    project.name = name
    project.short_name = short_name
    project.priority = priority
    project.type = type
    project.description = description
    project.formal_basis = formal_basis
    project.project_justification = project_justification
    project.additional_info = additional_info
    project.project_goals = project_goals
    project.risks = risks
    project.deviations = deviations
    project.last_change_date = date.today()
    project.save()

    new_project_data = Project.fetch(Project.id == project_id)[0].get_dto()

    documents = ProjectDocument.fetch(ProjectDocument.project == project)
    documents = [doc.get_dto() for doc in documents]

    return {**new_project_data, 'documents': documents}, {**prev_project_data, 'documents': documents}


def add_user_role(user_id: int, role_id: int, project_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectRole.get_or_none(ProjectRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    user_role = ProjectUserRole.get_or_none(user=user, role=role, project=project)
    if user_role:
        raise ApiError.BadRequest('User has already been assigned to this role')

    project_user_role = ProjectUserRole(user=user, role=role, project=project)
    project_user_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def remove_user_role(user_id: int, role_id: int, project_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectRole.get_or_none(ProjectRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    user_role = ProjectUserRole.get_or_none(user=user, role=role, project=project)
    if not user_role:
        raise ApiError.BadRequest('User is not assigned to this role')

    ProjectUserRole.delete().where(ProjectUserRole.id == user_role).execute()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def create_indicator(
        project_id: int, name: str, evaluation_type: str, evaluation_frequency: str,
        units_measure: str, base_value: int, base_value_date: date, description: str, info_collection: str,
        coverage_units: str, approval_doc: str
):
    if evaluation_type not in indicator_evaluation_list:
        ApiError.BadRequest('Evaluation type not found')

    if coverage_units not in coverage_list:
        ApiError.BadRequest('Coverage units not found')

    if base_value_date == '0000-00-00':
        base_value_date = None

    indicator = ProjectIndicators(
        project=project_id,
        name=name,
        evaluation_type=evaluation_type,
        evaluation_frequency=evaluation_frequency,
        units_measure=units_measure,
        base_value=base_value,
        base_value_date=base_value_date,
        description=description,
        info_collection=info_collection,
        coverage_units=coverage_units,
        approval_doc=approval_doc
    )
    indicator.save()
    return indicator.get_dto()


def indicator_set_user_role(user_id: int, indicator_role_id: int, indicator_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectIndicatorsRole.get_or_none(ProjectIndicatorsRole.id == indicator_role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    indicator = ProjectIndicators.get_or_none(ProjectIndicators.id == indicator_id)
    if not indicator:
        raise ApiError.BadRequest('Indicator not found')

    indicator_user_role = ProjectIndicatorsUserRole(user=user, role=role, indicator=indicator)
    indicator_user_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def indicator_remove_user_role(user_id: int, role_id: int, indicator_id: int):
    user = User.get_or_none(id=user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    indicator = ProjectIndicators.get_or_none(id=indicator_id)
    if not indicator:
        raise ApiError.BadRequest('Indicator not found')

    role = ProjectIndicatorsRole.get_or_none(id=role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    user_role = ProjectIndicatorsUserRole.get_or_none(user=user, role=role, indicator=indicator)
    if not user_role:
        raise ApiError.BadRequest('User is not assigned to this role')

    ProjectIndicatorsUserRole.delete().where(ProjectIndicatorsUserRole.id == user_role).execute()
    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def get_indicators(project_id: int):
    indicators = [indicator.get_dto() for indicator in ProjectIndicators.fetch(ProjectIndicators.project == project_id)]
    indicators_value = [value.get_dto() for value in
                        ProjectIndicatorsValues.select().join(ProjectIndicators).where(
                            ProjectIndicators.project == project_id,
                            ProjectIndicatorsValues.period.month == date.today().month,
                            ProjectIndicatorsValues.period.year == date.today().year)]

    new_indicators = []
    for indicator in indicators:
        indicator['status'] = 'AWAITING'
        for value in indicators_value:
            if value['indicator']['id'] == indicator['id']:
                indicator['actual_value'] = value['actual_value']
                indicator['forecast_value'] = value['forecast_value']
                indicator['plan_value'] = value['plan_value']
                indicator['status'] = value['status']
        new_indicators.append(indicator)

    return new_indicators


def get_indicator(indicator_id: int):
    indicator = ProjectIndicators.fetch(ProjectIndicators.id == indicator_id)[0].get_dto()
    indicator_values = [value.get_dto() for value in
                        ProjectIndicatorsValues.select().where(ProjectIndicatorsValues.indicator == indicator_id)
                        ]

    indicator['indicator_values'] = indicator_values

    indicator['status'] = 'AWAITING'
    for value in indicator_values:
        if value['period'].month == date.today().month and value['period'].year == date.today().year:
            indicator['status'] = value['status']

    return indicator


def update_indicator(
        indicator_id: int, name: str, evaluation_type: str,
        evaluation_frequency: date, units_measure: str, base_value: int,
        base_value_date: date, description: str, info_collection: str,
        coverage_units: str, approval_doc: str
):
    indicator = ProjectIndicators.get_or_none(ProjectIndicators.id == indicator_id)
    if not indicator:
        raise ApiError.BadRequest('Indicator not found')

    if evaluation_type not in indicator_evaluation_list:
        ApiError.BadRequest('Evaluation type not found')

    if coverage_units not in coverage_list:
        ApiError.BadRequest('Coverage units not found')

    prev_indicator_data = ProjectIndicators.fetch(ProjectIndicators.id == indicator_id)[0].get_dto()

    indicator.name = name
    indicator.evaluation_type = evaluation_type
    indicator.evaluation_frequency = evaluation_frequency
    indicator.units_measure = units_measure
    indicator.base_value = base_value
    indicator.base_value_date = base_value_date
    indicator.description = description
    indicator.info_collection = info_collection
    indicator.coverage_units = coverage_units
    indicator.approval_doc = approval_doc
    indicator.save()

    indicator_model = ProjectIndicators.fetch(ProjectIndicators.id == indicator_id)[0]
    indicator = indicator_model.get_dto()

    new_indicator_data = indicator_model.get_dto()

    indicator_values = [value.get_dto() for value in ProjectIndicatorsValues.select().where(ProjectIndicatorsValues.indicator == indicator_id)]

    indicator['indicator_values'] = indicator_values

    indicator['status'] = 'AWAITING'
    for value in indicator_values:
        if value['period'].month == date.today().month and value['period'].year == date.today().year:
            indicator['status'] = value['status']

    return indicator, new_indicator_data, prev_indicator_data


def delete_indicator(indicator_id: int):
    try:
        indicator = ProjectIndicators.fetch(ProjectIndicators.id == indicator_id)[0]
    except IndexError:
        return

    ProjectIndicators.delete().where(ProjectIndicators.id == indicator_id).execute()
    return indicator.get_dto()


def get_my_projects(user):
    projects = Project.fetch(ProjectUserRole.user == user.id)
    return [project.get_dto() for project in projects if not project.is_Archived]


def get_archive_projects():
    projects = Project.fetch(Project.is_Archived == True)
    if not projects:
        raise ApiError.BadRequest('Projects not found')
    return [project.get_dto() for project in projects]


def get_archive_my_projects(user):
    projects = Project.fetch(ProjectUserRole.user == user.id)
    if not projects:
        raise ApiError.BadRequest('Projects not found')
    return [project.get_dto() for project in projects if project.is_Archived]


def get_roles():
    roles = ProjectRole.select()
    return [role.get_dto() for role in roles]


def create_indicator_value(indicator_id: int, period: date, plan: str, forecast: str, actual: str):
    indicator = ProjectIndicators.get_or_none(ProjectIndicators.id == indicator_id)
    if not indicator:
        raise ApiError.BadRequest('Indicator not found')

    if actual == '':
        status = 'AWAITING'
    elif actual >= plan:
        status = 'ACHIEVED'
    else:
        status = 'DISRUPTION'

    indicator_value = ProjectIndicatorsValues(
        indicator=indicator_id,
        period=period,
        plan=plan,
        forecast=forecast,
        actual=actual,
        status=status
    )
    indicator_value.save()
    return indicator_value.get_dto()


def update_indicator_value(indicator_value_id: int, period: date, plan: str, forecast: str, actual: str):
    indicator_value = ProjectIndicatorsValues.get_or_none(ProjectIndicatorsValues.id == indicator_value_id)
    if not indicator_value:
        raise ApiError.BadRequest('Indicator value not found')

    if actual == '':
        status = 'AWAITING'
    elif actual >= plan:
        status = 'ACHIEVED'
    else:
        status = 'DISRUPTION'

    prev_indicator_value_data = indicator_value.get_dto()

    indicator_value.period = period
    indicator_value.plan = plan
    indicator_value.forecast = forecast
    indicator_value.actual = actual
    indicator_value.status = status
    indicator_value.save()

    indicator_value_data = indicator_value.get_dto()

    return indicator_value_data, prev_indicator_value_data


def delete_indicator_value(indicator_value_id: int):
    indicator_value = ProjectIndicatorsValues.get_or_none(ProjectIndicatorsValues.id == indicator_value_id)
    if not indicator_value:
        return

    ProjectIndicatorsValues.delete().where(ProjectIndicatorsValues.id == indicator_value_id).execute()
    return indicator_value.get_dto()


def get_indicator_value(indicator_value_id):
    indicator_value = ProjectIndicatorsValues.get_or_none(ProjectIndicatorsValues.id == indicator_value_id)
    if not indicator_value:
        raise ApiError.BadRequest('Indicator value not found')

    return indicator_value.get_dto()


def get_indicator_roles():
    roles = [role.get_dto() for role in ProjectIndicatorsRole.select()]
    return roles


def save_file(file: FileStorage, project_id: int, file_type: str, user_id):
    project = Project.get_or_none(id=project_id)
    if not project:
        raise ApiError.BadRequest('Project not found')

    file = file_service.save_file(file)

    document = ProjectDocument(
        project=project,
        file=file,
        type=file_type
    )
    document.save()

    return document.get_dto()


def remove_file(file_id: str, project_id: int, user_id):
    document = ProjectDocument.get_or_none(project=project_id, file=file_id)
    if not document:
        raise ApiError.BadRequest('File not found')

    ProjectDocument.delete().where(ProjectDocument.id == document).execute()
    return document.get_dto()
