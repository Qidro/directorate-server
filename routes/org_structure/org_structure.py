from flask import Blueprint, request, jsonify, Response
from decorators import login_required, rights_required
from service import org_structer_services
from webargs import flaskparser
from .fields import create_department_model, edit_department_model, delete_department_model, create_position_model, \
    edit_position_model, delete_position_model


org_structure_router = Blueprint('org_structure', __name__)


@org_structure_router.get('/org_structure/departments')
def get_departments(user):
    departments = org_structer_services.get_departments()
    return jsonify(departments)


@org_structure_router.get('/org_structure/department/<int:department_id>')
def get_department(user, department_id):
    department = org_structer_services.get_department(department_id)
    return jsonify(department)


@org_structure_router.post('/org_structure/department/create')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def create_department(user):
    data = flaskparser.parser.parse(create_department_model, request)
    department = org_structer_services.create_department(data['name'])
    return jsonify(department)


@org_structure_router.post('/org_structure/department/edit')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def edit_department(user):
    data = flaskparser.parser.parse(edit_department_model, request)
    department = org_structer_services.edit_department(data['id'], data['name'])
    return jsonify(department)


@org_structure_router.delete('/org_structure/department/delete')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def delete_department(user):
    data = flaskparser.parser.parse(delete_department_model, request)
    org_structer_services.delete_department(data['id'])
    return Response(status=204)


@org_structure_router.get('/org_structure/positions')
@login_required
def get_positions(user):
    positions = org_structer_services.get_positions()
    return jsonify(positions)


@org_structure_router.get('/org_structure/position/<int:position_id>')
@login_required
def get_position(user, position_id):
    position = org_structer_services.get_position(position_id)
    return jsonify(position)


@org_structure_router.post('/org_structure/position/create')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def create_position(user):
    data = flaskparser.parser.parse(create_position_model, request)
    position = org_structer_services.create_position(data['name'], data['department_id'])
    return jsonify(position)


@org_structure_router.post('/org_structure/position/edit')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def edit_position(user):
    data = flaskparser.parser.parse(edit_position_model, request)
    position = org_structer_services.edit_position(data['id'], data['name'])
    return jsonify(position)


@org_structure_router.delete('/org_structure/position/delete')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def delete_position(user):
    data = flaskparser.parser.parse(delete_position_model, request)
    org_structer_services.delete_position(data['id'])
    return Response(status=204)
