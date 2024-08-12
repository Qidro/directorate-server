from flask import Blueprint, jsonify
from service import project_resources_service
from decorators import login_required

project_resources_router = Blueprint('project_resources', __name__)


@project_resources_router.get('/project/<project_id>/resource_working')
@login_required
def get_resource_working(user, project_id):
    resources = project_resources_service.get_resource_working(project_id)
    return jsonify(resources)


@project_resources_router.get('/project/<project_id>/resource_cp')
@login_required
def get_resource_cp(user, project_id):
    resources = project_resources_service.get_resource_cp(project_id)
    return jsonify(resources)
