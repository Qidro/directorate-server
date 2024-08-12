from flask import Blueprint, jsonify, request, Response
from webargs import flaskparser
from .fields import set_expert_model, remove_expert_model, set_verdict_model, create_model, update_model, add_comment_model
from decorators import login_required, rights_required
from service import proposal_service
from service.log import proposal_log_service


proposal_router = Blueprint('proposal_router', __name__)


# create - works
@proposal_router.post('/proposal/create')
@login_required
def create(user):
    data = flaskparser.parser.parse(create_model, request)
    proposal = proposal_service.create(
        user.id, data['name'], data['realization_period_start'], data['realization_period_end'], data['executors'],
        data['justification'], data['purpose'], data['results'], data['target_indicators'],
        data['planned_actions'], data['resources'], data['contacts']
    )
    return jsonify(proposal)


@proposal_router.post('/proposal/update')
@login_required
def update(user):
    data = flaskparser.parser.parse(update_model, request)
    proposal, prev_proposal = proposal_service.update(
        data['id'], user.id, data['name'], data['realization_period_start'],
        data['realization_period_end'], data['executors'], data['justification'], data['purpose'], data['results'],
        data['target_indicators'], data['planned_actions'], data['resources'], data['contacts']
    )

    proposal_log_service.proposal_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        proposal_dto=proposal,
        prev_proposal_dto=prev_proposal,
        action='UPDATE_PROPOSAL'
    )

    return jsonify(proposal)


@proposal_router.get('/proposals')
@login_required
def get_my_proposals(user):
    proposals = proposal_service.get_my(user.id)
    return jsonify(proposals)


@proposal_router.get('/proposals/all')
@login_required
@rights_required(['DIRECTOR-EX', 'RECTOR'])
def get_all_proposals(user):
    proposals = proposal_service.get_all()
    return jsonify(proposals)


@proposal_router.get('/proposals/expert')
@login_required
@rights_required(['EXPERT-EX'])
def get_expert_proposals_(user):
    proposals = proposal_service.get_when_expert(user.id)
    return jsonify(proposals)


@proposal_router.get('/proposal/<proposal_id>')
@login_required
def get_proposal(user, proposal_id):
    proposal = proposal_service.get_proposal(proposal_id)
    return jsonify(proposal)


# Оставление комментариев экспертом
@proposal_router.post('/proposal/add_comment')
@login_required
@rights_required(['EXPERT-EX'])
def add_comment(user):
    data = flaskparser.parser.parse(add_comment_model, request)
    comment = proposal_service.add_comment(
        data['proposal'], user.id, data['status'], data['name'], data['realization_period'],
        data['executors'], data['justification'], data['purpose'], data['results'],
        data['target_indicators'], data['planned_actions'], data['resources'], data['contacts']
    )

    proposal_log_service.proposal_comment_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        proposal_id=data['proposal']
    )

    return jsonify(comment)


# Назначение на роль эсперта админом
@proposal_router.post('/proposal/expert/set')
@login_required
@rights_required(['DIRECTOR-EX'])
def set_expert(user):
    data = flaskparser.parser.parse(set_expert_model, request)
    expert = proposal_service.set_expert(data['proposal_id'], data['user_id'], user.id)

    proposal_log_service.proposal_expert_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        proposal_id=data['proposal_id'],
        expert_dto=expert,
        action='SET_EXPERT'
    )

    return jsonify(expert)


@proposal_router.delete('/proposal/expert/remove')
@login_required
@rights_required(['DIRECTOR-EX'])
def remove_expert(user):
    data = flaskparser.parser.parse(remove_expert_model, request)
    expert = proposal_service.remove_expert(data['proposal_id'], data['user_id'])

    proposal_log_service.proposal_expert_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        proposal_id=data['proposal_id'],
        expert_dto=expert,
        action='REMOVE_EXPERT'
    )

    return Response(status=204)


# Вынесение финального вердикта по ПП
@proposal_router.post('/proposal/verdict/set')
@login_required
@rights_required(['DIRECTOR-EX'])
def set_verdict(user):
    data = flaskparser.parser.parse(set_verdict_model, request)
    verdict = proposal_service.set_verdict(data['proposal_id'], user, data['conclusion'], data['status'])
    return jsonify(verdict)


# Возвращает список экспертов, которые еще не назначены на роль эксперта в ПП
@proposal_router.get('/proposal/<proposal_id>/experts')
@login_required
@rights_required(['DIRECTOR-EX'])
def get_experts(user, proposal_id):
    experts = proposal_service.get_experts(proposal_id)
    return jsonify(experts)


@proposal_router.get('/proposal/<int:proposal_id>/logs&position=<int:position>')
@login_required
def get_backpack_logs(user, proposal_id, position):
    logs = proposal_log_service.get_proposal_logs(proposal_id, position)
    return jsonify(logs)

