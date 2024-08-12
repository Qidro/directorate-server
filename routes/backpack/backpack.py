from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from decorators import login_required, file_required
from .fields import create_model, user_role_model, delete_model, update_model, \
    upload_file_model, remove_file_model
from service import backpack_service
from service.log import backpack_log_service

backpack_router = Blueprint('backpack', __name__)


@backpack_router.post('/backpack/create')
@login_required
def create(user):
    data = flaskparser.parser.parse(create_model, request)
    backpack = backpack_service.create(data['name'], data['description'])
    return jsonify(backpack)


@backpack_router.get('/backpack/<backpack_id>')
@login_required
def get_backpack(user, backpack_id):
    backpack = backpack_service.get(backpack_id)

    return jsonify(backpack)


@backpack_router.post('/backpack/user/role/set')
@login_required
def set_user_role(user):
    data = flaskparser.parser.parse(user_role_model, request)
    user_role = backpack_service.add_user_role(data['user_id'], data['role_id'], data['backpack_id'])

    backpack_log_service.backpack_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        backpack_id=data['backpack_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


@backpack_router.post('/backpack/update')
@login_required
def update(user):
    data = flaskparser.parser.parse(update_model, request)
    backpack, prev_backpack = backpack_service.update(data['backpack_id'], data['name'], data['description'])

    backpack_log_service.backpack_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        backpack_dto=backpack,
        prev_backpack_dto=prev_backpack,
        action='UPDATE_BACKPACK'
    )

    return jsonify(backpack)


@backpack_router.delete('/backpack/user/role/remove')
@login_required
def remove_user_role(user):
    data = flaskparser.parser.parse(user_role_model, request)
    removed_backpack = backpack_service.remove_user_role(data['user_id'], data['role_id'], data['backpack_id'])

    backpack_log_service.backpack_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        backpack_id=data['backpack_id'],
        user_role_dto=removed_backpack,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


@backpack_router.delete('/backpack/delete')
@login_required
def delete(user):
    data = flaskparser.parser.parse(delete_model, request)
    backpack_service.delete(data['backpack_id'])
    return Response(status=204)


@backpack_router.get('/backpacks')
@login_required
def get_my(user):
    backpack = backpack_service.get_my(user)
    return backpack


@backpack_router.get('/backpacks/all')
@login_required
def get_all(user):
    backpack_list = backpack_service.get_all()
    return jsonify(backpack_list)


@backpack_router.get('/backpack/roles')
@login_required
def get_roles(user):
    roles = backpack_service.get_roles()
    return roles


@backpack_router.get('/backpack/<backpack_id>/indicators')
@login_required
def get_indicators(user, backpack_id):
    indicators = backpack_service.get_indicators(backpack_id)
    return indicators


@backpack_router.get('/backpack/<backpack_id>/calendar_plans')
@login_required
def get_calendar_plan_points(user, backpack_id):
    points = backpack_service.get_calendar_plans(backpack_id)
    return points


@backpack_router.get('/backpack/<backpack_id>/contracts')
@login_required
def get_contracts(user, backpack_id):
    contracts = backpack_service.get_contracts(backpack_id)
    return contracts


@backpack_router.get('/backpack/<backpack_id>/budgets')
@login_required
def get_budget(user, backpack_id):
    budget = backpack_service.get_budgets(backpack_id)
    return budget


@backpack_router.post('/backpack/file/upload')
@login_required
@file_required()
def upload_file(file, user):
    data = flaskparser.parser.parse(upload_file_model, request, location='form')
    document = backpack_service.save_backpack_file(file, data['backpack_id'], data['type'])

    backpack_log_service.backpack_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        backpack_id=data['backpack_id'],
        file_dto=document,
        action='UPLOAD_FILE'
    )

    return jsonify(document)


@backpack_router.delete('/backpack/file/remove')
@login_required
def remove_file(user):
    data = flaskparser.parser.parse(remove_file_model, request)
    removed_document = backpack_service.remove_file(data['file_id'], data['backpack_id'])

    backpack_log_service.backpack_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        backpack_id=data['backpack_id'],
        file_dto=removed_document,
        action='REMOVE_FILE'
    )

    return Response(status=204)


@backpack_router.get('/backpack/<int:backpack_id>/logs&position=<int:position>')
@login_required
def get_backpack_logs(user, backpack_id, position):
    logs = backpack_log_service.get_backpack_logs(backpack_id, position)
    return jsonify(logs)
