from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from decorators import login_required, rights_required
from .fields import create_result_model, edit_result_model, set_result_user_role_model, result_value_model, \
    remove_result_model, remove_result_value_model, result_value_update_model
from service import project_results_service
from service.log import project_results_log_service


project_result_router = Blueprint('project_result', __name__)


@project_result_router.post('/project/result/create')
@login_required
def create_result(user):
    data = flaskparser.parser.parse(create_result_model, request)
    result = project_results_service.create_result(
        data['project_id'], data['name'], data['type'], data['units_measure'],
        data['characteristic'], data['approval_doc']
    )

    project_results_log_service.result_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        result_dto=result,
        action='CREATE_RESULT'
    )

    return jsonify(result)


@project_result_router.post('/project/result/edit')
@login_required
def edit_result(user):
    data = flaskparser.parser.parse(edit_result_model, request)
    result, prev_result = project_results_service.edit_result(
        data['result_id'], data['name'], data['type'], data['units_measure'],
        data['characteristic'], data['approval_doc'],
        data['status']
    )

    project_results_log_service.result_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        result_dto=result,
        prev_result_dto=prev_result,
        action='UPDATE_RESULT'
    )

    return jsonify(result)


@project_result_router.get('/project/result/all')
@login_required
def get_projects_results(user):
    result = project_results_service.get_all_results()
    return jsonify(result)


@project_result_router.delete('/project/result/remove')
@login_required
def remove_result(user):
    data = flaskparser.parser.parse(remove_result_model, request)
    result = project_results_service.remove_result(data['result_id'])

    if result:
        project_results_log_service.result_log(
            author_id=user.id,
            author_name=user.get_dto()['fullname'],
            result_dto=result,
            action='DELETE_RESULT'
        )

    return Response(status=204)


@project_result_router.post('/project/result/user/role/add')
@login_required
def add_user_role(user):
    data = flaskparser.parser.parse(set_result_user_role_model, request)
    user_role = project_results_service.result_set_user_role(
        data['user_id'], data['role_id'], data['project_result_id']
    )

    project_results_log_service.result_role_log(
        author_id=user.id,
        author_name=user.get_dto()["fullname"],
        result_id=data['project_result_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


@project_result_router.delete('/project/result/user/role/remove')
@login_required
def remove_user_role(user):
    data = flaskparser.parser.parse(set_result_user_role_model, request)
    removed_user_role = project_results_service.remove_result_role(data['user_id'], data['role_id'], data['project_result_id'])

    project_results_log_service.result_role_log(
        author_id=user.id,
        author_name=user.get_dto()["fullname"],
        result_id=data['project_result_id'],
        user_role_dto=removed_user_role,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


@project_result_router.get('/project/result/roles')
@login_required
def project_roles(user):
    roles = project_results_service.get_roles()
    return jsonify(roles)


@project_result_router.get('/project/result/<result_id>')
@login_required
def get_proposal(user, result_id):
    result = project_results_service.get_one_result(result_id)
    return jsonify(result)


@project_result_router.get('/project/<project_id>/results')
@login_required
def get_project_results(user, project_id):
    result = project_results_service.get_project_results(project_id)
    return jsonify(result)


@project_result_router.post("/project/result/value/add")
@login_required
def add_value(user):
    data = flaskparser.parser.parse(result_value_model, request)
    value = project_results_service.create_result_value(
        data['result_id'], data['achievement_date'],
        data['plan_value'], data['forecast_value']
    )

    project_results_log_service.value_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        value_dto=value,
        action='CREATE_VALUE'
    )

    return jsonify(value)


@project_result_router.post("/project/result/value/update")
@login_required
def edit_value(user):
    data = flaskparser.parser.parse(result_value_update_model, request)
    value, prev_value = project_results_service.update_result_value(
        data['value_id'], data['achievement_date'],
        data['plan_value'], data['forecast_value']
    )

    project_results_log_service.value_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        value_dto=value,
        prev_value_dto=prev_value,
        action='UPDATE_VALUE'
    )

    return jsonify(value)


@project_result_router.delete('/project/result/value/remove')
@login_required
def remove_result_value(user):
    data = flaskparser.parser.parse(remove_result_value_model, request)
    value = project_results_service.remove_result_value(data['value_id'])

    if value:
        project_results_log_service.value_log(
            author_id=user.id,
            author_name=user.get_dto()['fullname'],
            value_dto=value,
            action='REMOVE_VALUE'
        )

    return Response(status=204)


@project_result_router.get("/project/result/<result_id>/values/")
@login_required
def get_result_values(user, result_id):
    result = project_results_service.get_result_values(result_id)
    return jsonify(result)


@project_result_router.get('/project/result/<int:result_id>/logs&position=<int:position>')
@login_required
def get_backpack_logs(user, result_id, position):
    logs = project_results_log_service.get_results_logs(result_id, position)
    return jsonify(logs)
