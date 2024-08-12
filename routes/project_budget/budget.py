from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from decorators import login_required
from .fields import create_budget_model, edit_budget_model, delete_budget_model
from service import project_budget_service
from service.log import project_budget_log_service


budget_router = Blueprint('budget', __name__)


@budget_router.post('/budget/create')
@login_required
def create_budget(user):
    data = flaskparser.parser.parse(create_budget_model, request)
    budget = project_budget_service.create_budget(data['project_id'], data['stage_id'], data['funding_source'],
                                                  data['costs_name'], data['spending_costs'])

    project_budget_log_service.budget_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        budget_dto=budget,
        action='CREATE_BUDGET'
    )

    return jsonify(budget)


@budget_router.post('/budget/edit')
@login_required
def edit_budget(user):
    data = flaskparser.parser.parse(edit_budget_model, request)
    budget, prev_budget = project_budget_service.edit_budget(data['budget_id'], data['funding_source'],
                                                             data['costs_name'], data['spending_costs'])

    project_budget_log_service.budget_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        budget_dto=budget,
        prev_budget_dto=prev_budget,
        action='UPDATE_BUDGET'
    )

    return jsonify(budget)


@budget_router.delete('/budget/delete')
@login_required
def delete_budget(user):
    data = flaskparser.parser.parse(delete_budget_model, request)
    deleted_budget = project_budget_service.delete_budget(data['budget_id'])

    project_budget_log_service.budget_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        budget_dto=deleted_budget,
        action='DELETE_BUDGET'
    )

    return Response(status=204)


@budget_router.get('/project/<project_id>/budgets')
@login_required
def get_budgets(user, project_id):
    budgets = project_budget_service.get_budgets(project_id)
    return jsonify(budgets)


@budget_router.get('/budget/<budget_id>')
@login_required
def get_budget(user, budget_id):
    budget = project_budget_service.get_budget(budget_id)
    return jsonify(budget)



