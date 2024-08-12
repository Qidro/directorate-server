from models import ProjectCalendarPlan, ProjectBudget
from exceptions import ApiError
from constants.constants import budget_costs_list


def create_budget(project_id: int, stage_id: int, funding_source: str, costs_name: str, spending_costs: float):
    calendar_point = ProjectCalendarPlan.get_or_none(ProjectCalendarPlan.id == stage_id)
    if not calendar_point:
        raise ApiError.BadRequest('Calendar point not found')

    if calendar_point.type != 'STAGE':
        raise ApiError.BadRequest('Calendar point no type stage')

    if costs_name not in budget_costs_list:
        raise ApiError.BadRequest('Costs not found')

    if spending_costs < 0:
        raise ApiError.BadRequest('Costs can not be negative')

    budget = ProjectBudget(
        project=project_id,
        stage=stage_id,
        funding_source=funding_source,
        costs_name=costs_name,
        spending_costs=spending_costs
    )
    budget.save()

    return budget.get_dto()


def edit_budget(budget_id: int, funding_source: str, costs_name: str, spending_costs: float):
    budget = ProjectBudget.get_or_none(ProjectBudget.id == budget_id)
    if not budget:
        raise ApiError.BadRequest('Budget not found')

    if costs_name not in budget_costs_list:
        raise ApiError.BadRequest('Costs not found')

    prev_budget_data = budget.get_dto()

    budget.funding_source = funding_source
    budget.costs_name = costs_name
    budget.spending_costs = spending_costs
    budget.save()

    new_budget_data = budget.get_dto()

    return new_budget_data, prev_budget_data


def delete_budget(budget_id: int):
    budget = ProjectBudget.get_or_none(ProjectBudget.id == budget_id)
    if not budget:
        return

    ProjectBudget.delete().where(ProjectBudget.id == budget_id).execute()
    return budget.get_dto()


def get_budgets(project_id):
    budgets = ProjectBudget.select().where(ProjectBudget.project == project_id)
    return [budget.get_dto() for budget in budgets]


def get_budget(budget_id: int):
    budget = ProjectBudget.get_or_none(ProjectBudget.id == budget_id)
    if not budget:
        raise ApiError.BadRequest('Budget not found')

    return budget.get_dto()
