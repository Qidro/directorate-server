from flask import Blueprint, jsonify, request
from webargs import flaskparser
from decorators import login_required, rights_required
from service import archive_service
from .fields import backpack_model, project_model, proposal_model, user_model


archive_router = Blueprint('archive', __name__)


@archive_router.get('/archive/backpacks')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_backpacks(user):
    backpack = archive_service.get_backpacks_archive()
    return jsonify(backpack)


@archive_router.post('/archive/backpack/unzip')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def unzip_backpack(user):
    data = flaskparser.parser.parse(backpack_model, request)
    backpack = archive_service.unzip_backpack(data['backpack_id'])
    return jsonify(backpack)


@archive_router.get('/archive/projects')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_projects(user):
    projects = archive_service.get_projects_archive()
    return jsonify(projects)


@archive_router.post('/archive/project/unzip')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def unzip_project(user):
    data = flaskparser.parser.parse(project_model, request)
    project = archive_service.unzip_project(data['project_id'])
    return jsonify(project)


@archive_router.get('/archive/proposals')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_proposals(user):
    proposals = archive_service.get_proposals_archive()
    return jsonify(proposals)


@archive_router.post('/archive/proposal/unzip')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def unzip_proposal(user):
    data = flaskparser.parser.parse(proposal_model, request)
    proposal = archive_service.unzip_proposal(data['proposal_id'])
    return jsonify(proposal)


@archive_router.get('/archive/users')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_user(user):
    users = archive_service.get_user_archive()
    return jsonify(users)


@archive_router.post('/archive/user/unzip')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def unzip_user(user):
    data = flaskparser.parser.parse(user_model, request)
    user = archive_service.unzip_user(data['user_id'])
    return jsonify(user)
