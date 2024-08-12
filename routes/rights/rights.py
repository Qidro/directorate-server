from flask import Blueprint, jsonify
from decorators import login_required, rights_required
from service import rights_service

rights_router = Blueprint('rights', __name__)


@rights_router.get('/rights')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_rights(user):
    rights = rights_service.get_rights()
    return jsonify(rights)
