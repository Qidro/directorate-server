from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from .fields import create_contract_model, edit_contract_model, remove_contract_model, set_user_role_model, \
    set_stage_model, upload_file_model, remove_file_model
from decorators import login_required, file_required
from service import project_contract_services, file_service
from service.log import project_contract_log_services

project_contract_router = Blueprint('project_contract', __name__)


@project_contract_router.post('/project/contract/create')
@login_required
def create_contract(user):
    data = flaskparser.parser.parse(create_contract_model, request)
    contract = project_contract_services.create_contract(
        data['project_id'], data['name'], data['type'], data['federal_law'],
        data['planned_cost'], data['cost'], data['paid'], data['description'], data['link']
    )

    project_contract_log_services.contract_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_dto=contract,
        action='CREATE_CONTRACT'
    )

    return jsonify(contract)


@project_contract_router.post('/project/contract/edit')
@login_required
def edit_contract(user):
    data = flaskparser.parser.parse(edit_contract_model, request)
    contract, prev_contract = project_contract_services.edit_contract(
        data['contract_id'], data['name'], data['type'], data['federal_law'],
        data['planned_cost'], data['cost'], data['paid'], data['description'], data['link']
    )

    project_contract_log_services.contract_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_dto=contract,
        prev_contract_dto=prev_contract,
        action='UPDATE_CONTRACT'
    )

    return jsonify(contract)


@project_contract_router.delete('/project/contract/remove')
@login_required
def remove_contract(user):
    data = flaskparser.parser.parse(remove_contract_model, request)
    deleted_contract = project_contract_services.remove_contract(data['contract_id'])

    project_contract_log_services.contract_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_dto=deleted_contract,
        action='DELETE_CONTRACT'
    )

    return Response(status=204)


@project_contract_router.get('/project/<project_id>/contracts')
@login_required
def get_contracts(user, project_id):
    contracts = project_contract_services.get_contracts(project_id)
    return jsonify(contracts)


@project_contract_router.get('/project/contract/<contract_id>')
@login_required
def get_contract_by_id(user, contract_id):
    contract = project_contract_services.get_contract(contract_id)
    return jsonify(contract)


@project_contract_router.post('/project/contract/user/role/add')
@login_required
def set_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_contract_services.set_user_role_contract(
        data['contract_id'], data['user_id'], data['role_id']
    )

    project_contract_log_services.contract_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_id=data['contract_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


@project_contract_router.delete('/project/contract/user/role/remove')
@login_required
def remove_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_contract_services.remove_user_role_contract(
        data['contract_id'], data['user_id'], data['role_id']
    )

    project_contract_log_services.contract_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_id=data['contract_id'],
        user_role_dto=user_role,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


@project_contract_router.post('/project/contract/stage/edit')
@login_required
def edit_stage(user):
    data = flaskparser.parser.parse(set_stage_model, request)
    contract_stage = project_contract_services.edit_stage(data['contract_id'], data['status'])

    project_contract_log_services.contract_stage_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_id=data['contract_id']
    )

    return jsonify(contract_stage)


@project_contract_router.get('/project/contracts/roles')
@login_required
def get_roles(user):
    roles = project_contract_services.get_roles()
    return jsonify(roles)


@project_contract_router.post('/project/contract/file/upload')
@login_required
@file_required()
def upload_file(file, user):
    data = flaskparser.parser.parse(upload_file_model, request, location='form')
    document = project_contract_services.save_file(file, data['contract_id'], data['type'])

    project_contract_log_services.contract_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_id=data['contract_id'],
        file_dto=document,
        action='UPLOAD_FILE'
    )

    return jsonify(document)


@project_contract_router.delete('/project/contract/file/remove')
@login_required
def remove_file(user):
    data = flaskparser.parser.parse(remove_file_model, request)
    removed_document = project_contract_services.remove_file(data['file_id'], data['contract_id'])

    project_contract_log_services.contract_file_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        contract_id=data['contract_id'],
        file_dto=removed_document,
        action='REMOVE_FILE'
    )

    return Response(status=204)


@project_contract_router.get('/project/contract/<int:contract_id>/logs&position=<int:position>')
@login_required
def get_backpack_logs(user, contract_id, position):
    logs = project_contract_log_services.get_contract_logs(contract_id, position)
    return jsonify(logs)
