from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from .fields import create_model, delete_model, update_model, update_stage_model, set_user_role_model, \
    create_indicator_model, indicator_set_user_role_model, update_indicator_model, indicator_delete_model, \
    create_indicator_value_model, update_indicator_value_model, delete_indicator_value_model, \
    indicator_remove_user_role_model, upload_file_model, remove_file_model
from decorators import login_required, rights_required, file_required
from service import project_service
from service.log import project_log_service, project_indicator_log_service

project_router = Blueprint('project', __name__)


@project_router.get('/project/<project_id>')
@login_required
def get_project(user, project_id):
    project = project_service.get_project(user, project_id)
    return jsonify(project)


# Создание проекта
@project_router.post('/project/create')
@login_required
def create_project(user):
    data = flaskparser.parser.parse(create_model, request)
    project = project_service.create(data['proposal_id'], data['backpack_id'], data['user_id'], data['user_curator_id'])

    project_log_service.project_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_dto=project,
        action='CREATE_PROJECT'
    )

    return jsonify(project)


# Изменение статуса проекта
@project_router.post('/project/stage/update')
@login_required
def update_stage(user):
    data = flaskparser.parser.parse(update_stage_model, request)
    project = project_service.update_stage(data['project_id'], data['status'], user)

    project_log_service.project_stage_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_id=data['project_id'],
        new_status=project['status']
    )

    return jsonify(project)


# Получеине всех не архивных проектов
@project_router.get('/projects/all')
@login_required
def get_projects(user):
    projects = project_service.get_projects()
    return jsonify(projects)


# Удаление (архивация) проектов
@project_router.delete('/project/delete')
@login_required
def delete_project(user):
    data = flaskparser.parser.parse(delete_model, request)
    project_service.delete(data['id'])
    return Response(status=204)


# Изменение проекта
@project_router.post('/project/update')
@login_required
def update(user):
    data = flaskparser.parser.parse(update_model, request)
    project, prev_project = project_service.update(
        data['project_id'], data['name'], data['short_name'], data['priority'], data['type'], data['description'],
        data['formal_basis'], data['project_justification'], data['additional_info'], data['project_goals'],
        data['risks'], data['deviations']
    )

    project_log_service.project_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_dto=project,
        prev_project_dto=prev_project,
        action='UPDATE_PROJECT'
    )

    return jsonify(project)


# Добавление роли юзеру
@project_router.post('/project/user/role/add')
@login_required
def add_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_service.add_user_role(data['user_id'], data['role_id'], data['project_id'])

    project_log_service.project_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_id=data['project_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


# Удаление роли у юзера
@project_router.delete('/project/user/role/remove')
@login_required
def remove_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_service.remove_user_role(data['user_id'], data['role_id'], data['project_id'])

    project_log_service.project_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_id=data['project_id'],
        user_role_dto=user_role,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


# Создание показателя для проекта
@project_router.post('/project/indicator/create')
@login_required
def create_indicator(user):
    data = flaskparser.parser.parse(create_indicator_model, request)
    indicator = project_service.create_indicator(
        data['project_id'], data['name'], data['evaluation_type'], data['evaluation_frequency'],
        data['units_measure'], data['base_value'], data['base_value_date'], data['description'],
        data['info_collection'], data['coverage_units'], data['approval_doc']
    )

    project_indicator_log_service.indicator_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        indicator_dto=indicator,
        action='CREATE_INDICATOR'
    )

    return jsonify(indicator)


# Изменение показателя проекта
@project_router.post('/project/indicator/update')
@login_required
def update_indicator(user):
    data = flaskparser.parser.parse(update_indicator_model, request)
    indicator, new_indicator, prev_indicator = project_service.update_indicator(
        data['indicator_id'], data['name'], data['evaluation_type'], data['evaluation_frequency'],
        data['units_measure'], data['base_value'], data['base_value_date'], data['description'],
        data['info_collection'], data['coverage_units'], data['approval_doc']
    )

    project_indicator_log_service.indicator_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        indicator_dto=new_indicator,
        prev_indicator_dto=prev_indicator,
        action='UPDATE_INDICATOR'
    )

    return jsonify(indicator)


# Назначение юзера на показатель
@project_router.post('/project/indicator/user/role/add')
@login_required
def indicator_set_user_role(user):
    data = flaskparser.parser.parse(indicator_set_user_role_model, request)
    user_role = project_service.indicator_set_user_role(data['user_id'], data['indicator_role_id'],
                                                        data['indicator_id'])

    project_indicator_log_service.indicator_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        indicator_id=data['indicator_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


@project_router.delete('/project/indicator/user/role/remove')
@login_required
def indicator_remove_user_role(user):
    data = flaskparser.parser.parse(indicator_remove_user_role_model, request)
    user_role = project_service.indicator_remove_user_role(data['user_id'], data['indicator_role_id'], data['indicator_id'])

    project_indicator_log_service.indicator_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        indicator_id=data['indicator_id'],
        user_role_dto=user_role,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


# Получение всех показателей в выбранном проекте
@project_router.get('/project/<project_id>/indicators')
@login_required
def get_indicators(user, project_id):
    indicators = project_service.get_indicators(project_id)
    return jsonify(indicators)


@project_router.get('/project/indicator/<indicator_id>')
@login_required
def get_indicator(user, indicator_id):
    indicator = project_service.get_indicator(indicator_id)
    return jsonify(indicator)


# Полное удаление показателя из БД
@project_router.delete('/project/indicator/delete')
@login_required
def delete_indicator(user):
    data = flaskparser.parser.parse(indicator_delete_model, request)
    deleted_indicator = project_service.delete_indicator(data['indicator_id'])

    project_indicator_log_service.indicator_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        indicator_dto=deleted_indicator,
        action='DELETE_INDICATOR'
    )

    return Response(status=204)


# Получение Моих проектов(Если назначен хоть на 1 роль)
@project_router.get('/projects')
@login_required
def get_my_projects(user):
    projects = project_service.get_my_projects(user)
    return jsonify(projects)


@project_router.get('/project/roles')
@login_required
def project_roles(user):
    roles = project_service.get_roles()
    return jsonify(roles)


@project_router.post('/project/indicator/value/create')
@login_required
def create_indicator_value(user):
    data = flaskparser.parser.parse(create_indicator_value_model, request)
    indicator_value = project_service.create_indicator_value(
        data['indicator_id'], data['period'], data['plan_value'],
        data['forecast_value'], data['actual_value'])

    project_indicator_log_service.indicator_values_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        value_dto=indicator_value,
        action='CREATE_VALUE'
    )

    return jsonify(indicator_value)


@project_router.post('/project/indicator/value/update')
@login_required
def update_indicator_value(user):
    data = flaskparser.parser.parse(update_indicator_value_model, request)
    indicator_value, prev_indicator_value = project_service.update_indicator_value(
        data['indicator_value_id'], data['period'], data['plan_value'],
        data['forecast_value'], data['actual_value'])

    project_indicator_log_service.indicator_values_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        value_dto=indicator_value,
        prev_value_dto=prev_indicator_value,
        action='UPDATE_VALUE'
    )

    return jsonify(indicator_value)


@project_router.delete('/project/indicator/value/delete')
@login_required
def delete_indicator_value(user):
    data = flaskparser.parser.parse(delete_indicator_value_model, request)
    deleted_value = project_service.delete_indicator_value(data['indicator_value_id'])

    project_indicator_log_service.indicator_values_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        value_dto=deleted_value,
        action='DELETE_VALUE'
    )

    return Response(status=204)


@project_router.get('/project/indicator/value/<indicator_value_id>')
@login_required
def get_indicator_value(user, indicator_value_id):
    indicator_value = project_service.get_indicator_value(indicator_value_id)
    return jsonify(indicator_value)


@project_router.get('/project/indicator/roles')
@login_required
def get_indicator_roles(user):
    roles = project_service.get_indicator_roles()
    return jsonify(roles)


@project_router.post('/project/file/upload')
@login_required
@file_required()
def upload_file(file, user):
    data = flaskparser.parser.parse(upload_file_model, request, location='form')
    document = project_service.save_file(file, data['project_id'], data['type'], user)

    project_log_service.project_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_id=data['project_id'],
        file_dto=document,
        action='UPLOAD_FILE'
    )

    return jsonify(document)


@project_router.delete('/project/file/remove')
@login_required
def remove_file(user):
    data = flaskparser.parser.parse(remove_file_model, request)
    document = project_service.remove_file(data['file_id'], data['project_id'], user)

    project_log_service.project_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        project_id=data['project_id'],
        file_dto=document,
        action='REMOVE_FILE'
    )

    return Response(status=204)


@project_router.get('/project/indicator/<int:indicator_id>/logs&position=<int:position>')
@login_required
def get_indicator_logs(user, indicator_id, position):
    logs = project_indicator_log_service.get_indicator_logs(indicator_id, position)
    return jsonify(logs)


@project_router.get('/project/<int:project_id>/logs&position=<int:position>')
@login_required
def get_project_logs(user, project_id, position):
    logs = project_log_service.get_project_logs(project_id, position)
    return jsonify(logs)
