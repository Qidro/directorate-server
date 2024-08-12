from flask import Blueprint, send_file
from decorators import login_required
from service import generation_services

generation_router = Blueprint('generation', __name__)


@generation_router.get('/generation/proposal/<int:proposal_id>')
@login_required
def generate_proposal(user, proposal_id):
    file_stream, proposal_name = generation_services.generate_proposal(proposal_id)
    return send_file(file_stream, as_attachment=True, download_name=f'Проектное предложение. {proposal_name}.docx')


@generation_router.get('/generation/proposal_w_comments/<int:proposal_id>')
@login_required
def generate_proposal_w_comments(user, proposal_id):
    file_stream, proposal_name = generation_services.generate_proposal_w_comments(proposal_id)
    return send_file(file_stream, as_attachment=True, download_name=f'Проектное предложение. {proposal_name}.docx')


@generation_router.get('/generation/passport/<int:project_id>')
@login_required
def generate_passport(user, project_id):
    file_stream, passport_name = generation_services.generate_passport(project_id)
    return send_file(file_stream, as_attachment=True, download_name=f'Паспорт проекта. {passport_name}.docx')


@generation_router.get('/generation/plan/<int:project_id>')
@login_required
def generate_plan(user, project_id):
    file_stream, plan_name = generation_services.generate_plan(project_id)
    return send_file(file_stream, as_attachment=True, download_name=f'План проекта. {plan_name}.docx')
