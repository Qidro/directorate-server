import datetime
import io
from docxtpl import DocxTemplate
from exceptions import ApiError
from models import Proposal, Project, ProjectUserRole, ProposalComment, ProjectIndicators, ProjectResults, User, \
    ProjectRole, ProjectCalendarPlan, ProjectIndicatorsValues, ProjectBudget, ProjectCalendarPlanResults
from constants.constants import calendar_plan_dict


# Генерация ПП
def generate_proposal(proposal_id: int):
    document = DocxTemplate("layouts/proposal.docx")

    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest("Proposal not found")

    context = {
        'name': proposal.name,
        'realization_period': f'{proposal.realization_period_start.strftime("%d.%m.%Y")} - {proposal.realization_period_end.strftime("%d.%m.%Y")}',
        'executors': proposal.executors,
        'justification': proposal.justification,
        'purpose': proposal.purpose,
        'results': proposal.results,
        'target_indicators': proposal.target_indicators,
        'planned_actions': proposal.planned_actions,
        'resources': proposal.resources,
        'contacts': proposal.contacts,
        'current_date': datetime.date.today().strftime('%d.%m.%Y')
    }
    document.render(context)

    file_stream = io.BytesIO()
    document.save(file_stream)
    file_stream.seek(0)

    return file_stream, proposal.name


# Генерация ПП с комментариями
def generate_proposal_w_comments(proposal_id: int):
    document = DocxTemplate("layouts/proposal_w_сomments.docx")
    general_info = []
    project_info = []

    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest("Proposal not found")

    if ProposalComment.get_or_none(ProposalComment.proposal_id == proposal_id) is not None:
        comments = ProposalComment.select().where(ProposalComment.proposal == proposal_id)
        comment_gto = [comment.get_dto() for comment in comments]

        general_info = [
            {
                'row_name': '',
                'cols': [comment['user']['fullname'] for comment in comment_gto]
            },
            {
                'row_name': 'Наименование проекта',
                'label': proposal.name,
                'cols': [comment['name'] for comment in comment_gto]
            },
            {
                'row_name': 'Срок реализации проекта',
                'label': f'{proposal.realization_period_start.strftime("%d.%m.%Y")} - {proposal.realization_period_end.strftime("%d.%m.%Y")}',
                'cols': [comment['realization_period'] for comment in comment_gto]
            },
            {
                'row_name': 'Исполнители проекта',
                'label': proposal.executors,
                'cols': [comment['executors'] for comment in comment_gto]
            }
        ]
        project_info = [
            {
                'row_name': 'Обоснование проекта',
                'label': proposal.justification,
                'cols': [comment['justification'] for comment in comment_gto]
            },
            {
                'row_name': 'Цель проекта',
                'label': proposal.purpose,
                'cols': [comment['purpose'] for comment in comment_gto]
            },
            {
                'row_name': 'Результаты проекта',
                'label': proposal.results,
                'cols': [comment['results'] for comment in comment_gto]
            },
            {
                'row_name': 'Целевые показатели проекта ',
                'label': proposal.target_indicators,
                'cols': [comment['target_indicators'] for comment in comment_gto]
            },
            {
                'row_name': 'Описание планируемых действий',
                'label': proposal.planned_actions,
                'cols': [comment['planned_actions'] for comment in comment_gto]
            },
            {
                'row_name': 'Оценочные ресурсы проекта',
                'label': proposal.resources,
                'cols': [comment['resources'] for comment in comment_gto]
            },
            {
                'row_name': 'Контакты',
                'label': proposal.contacts,
                'cols': [comment['contacts'] for comment in comment_gto]
            }
        ]

    context = {
        'general_info': general_info,
        'project_info': project_info,
        'current_date': datetime.date.today().strftime('%d.%m.%Y')
    }
    document.render(context)

    file_stream = io.BytesIO()
    document.save(file_stream)
    file_stream.seek(0)

    return file_stream, proposal.name


# Генерация Паспорта
def generate_passport(project_id):
    document = DocxTemplate("layouts/passport.docx")
    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest("Project not found")

    # Основные положения и титул
    command_data = []

    command = ProjectUserRole.get_or_none(ProjectUserRole.project == project_id)

    if command is not None:
        curator = [user_data.get_dto() for user_data in
                   User.fetch(User.id == command.get_or_none(ProjectUserRole.role == 2).user.id)]
        supervisor = [user_data.get_dto() for user_data in
                      User.fetch(User.id == command.get_or_none(ProjectUserRole.role == 3).user.id)]

        project_data = [data.get_dto() for data in Project.fetch(Project.id == project_id)][0]
        role_name = [role_name.get_dto() for role_name in ProjectRole.select()]

        for role in role_name:
            user_role = []
            for user in project_data['users']:
                if role['id'] == user['role']['id']:
                    user_role.append(user['fullname'])
            if user_role:
                command_data.append(f"{role['name']}: {', '.join(user_role)}")

    project_dto = project.get_dto()

    title = {
        'name': project.name,
        'project_justification': project.project_justification,
        'formal_basis': project.formal_basis,
        'start_date': datetime.datetime.strptime(project_dto['start_date'], '%Y-%m-%d').strftime(
            '%d.%m.%Y') if project_dto['start_date'] is not None else ' ',
        'end_date': datetime.datetime.strptime(project_dto['end_date'], '%Y-%m-%d').strftime(
            '%d.%m.%Y') if project_dto['end_date'] is not None else ' ',
        'curator': curator[0]['fullname'] if command is not None else ' ',
        'supervisor': supervisor[0]['fullname'] if command is not None else ' ',
        'command': '\n'.join(command_data) if command is not None else ' '
    }

    # Содержание проекта
    indicators = ProjectIndicators.select().where(ProjectIndicators.project_id == project_id)
    indicators_data = [indicator.get_dto() for indicator in indicators]
    indicators = []
    number_periods = []
    for indicator in indicators_data:
        indicator_values = ProjectIndicatorsValues.select().where(
            ProjectIndicatorsValues.indicator_id == indicator['id'])
        indicator_values = [indicator_value.get_dto() for indicator_value in indicator_values]

        if indicator_values:
            number_periods.append(len(indicator_values))

            indicator_value = [indicator_value['actual_value'] for indicator_value in indicator_values]

            indicators.append({
                'row_name': indicator['name'],
                'base_value': indicator['base_value'],
                'cols': indicator_value
            })

    for indicator in indicators:
        for index in range(max(number_periods)):
            try:
                indicator['cols'][index]
            except:
                indicator['cols'].append(' ')

    project_results = [results.name for results in ProjectResults.fetch(ProjectResults.project == project_id)]
    project_results = "\n".join(project_results)
    if number_periods:
        number_periods = [number + 1 for number in range(max(number_periods))]
    else:
        number_periods = ' '
    project_content = {
        'number_periods': number_periods,
        'project_goals': project.project_goals,
        'project_results': project_results,
        'deviations': project.deviations,
        'indicators': indicators
    }

    # Способы достижения целей и задач проекта
    achieve_goals = []
    number = 0

    calendar_plans = [plan.get_dto() for plan in ProjectCalendarPlan.fetch(ProjectCalendarPlan.project == project_id)]

    for calendar_plan in calendar_plans:
        for plan_type in calendar_plan_dict:
            if calendar_plan['type'] == plan_type:
                calendar_plan['type'] = calendar_plan_dict[plan_type]
        number += 1
        achieve_goal = {
            'number': number,
            'name': calendar_plan['name'],
            'type': calendar_plan['type'],
            'date': datetime.datetime.strptime(calendar_plan['end_date_fact'], '%Y-%m-%d').strftime(
                '%d.%m.%Y') if calendar_plan['end_date_fact'] is not None else ' ',

        }
        achieve_goals.append(achieve_goal)

    # Бюджет
    budget_number = []
    count_budget = []
    budget_data = []
    number = 0
    big_money = 0
    budgets_data = [budget.get_dto() for budget in ProjectBudget.fetch(ProjectBudget.project == project_id)]
    if budgets_data:
        for budget in budgets_data:
            if budget['stage']['id'] in count_budget:
                break
            else:
                count_budget.append(budget['stage']['id'])
                number += 1
                budget_number.append(number)

        wage = []
        overheads = []
        equipment = []
        consumables = []
        business_trips = []
        other = []

        for budget_id in count_budget:
            budget_calendar_plans = [budget.get_dto() for budget in ProjectBudget.fetch(ProjectBudget.stage == budget_id)]
            wage.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if budget_calendar_plan['costs_name'] == 'WAGE'])
            )
            overheads.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if budget_calendar_plan['costs_name'] == 'OVERHEADS'])
            )
            business_trips.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if budget_calendar_plan['costs_name'] == 'BUSINESS_TRIPS'])
            )
            consumables.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if budget_calendar_plan['costs_name'] == 'CONSUMABLES'])
            )
            equipment.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if budget_calendar_plan['costs_name'] == 'EQUIPMENT'])
            )
            other.append(
                sum([budget_calendar_plan['spending_costs']
                     for budget_calendar_plan
                     in budget_calendar_plans
                     if (budget_calendar_plan['costs_name'] == 'SOFTWARE' or
                         budget_calendar_plan['costs_name'] == 'EDUCATION')])
            )

        budget_data = [
            {
                'row_name': 'Зарплата*',
                'stage': wage,
                'total': sum(wage)
            },
            {
                'row_name': 'Накладные расходы*',
                'stage': overheads,
                'total': sum(overheads)
            },
            {
                'row_name': 'Командировки*',
                'stage': business_trips,
                'total': sum(business_trips)
            },
            {
                'row_name': 'Расходные материалы*',
                'stage': consumables,
                'total': sum(consumables)
            },
            {
                'row_name': 'Оборудование*',
                'stage': equipment,
                'total': sum(equipment)
            },
            {
                'row_name': 'др.',
                'stage': other,
                'total': sum(other)
            }
        ]

        big_money = round(sum(wage) + sum(overheads) + sum(business_trips) + sum(consumables) + sum(equipment) + sum(other),
                          2)

        if budget_number:
            budget_number = [number + 1 for number in range(max(budget_number))]
        else:
            budget_number = ' '

    document_data = title | project_content | {'achieve_goals': achieve_goals} | {'risks': project.risks} | \
                    {'additional_info': project.additional_info} | \
                    {'budget_number': budget_number} | \
                    {'budget': budget_data} | {'BIG_MONEY': big_money}

    document.render(document_data)

    file_stream = io.BytesIO()
    document.save(file_stream)
    file_stream.seek(0)

    return file_stream, project.name


# Генерация РАБотчего/Сводного плана
def generate_plan(project_id):
    document = DocxTemplate("layouts/plan.docx")

    project = Project.get_or_none(Project.id == project_id)
    if not project:
        raise ApiError.BadRequest("Project not found")

    # Титульник
    project_dto = project.get_dto()

    curator = []
    supervisor = []

    for user in project_dto['users']:
        if user['role']['slug'] == 'CURATOR':
            curator.append(user['fullname'] + ' - ' + user['role']['description'])
        if user['role']['slug'] == 'SUPERVISOR':
            supervisor.append(user['fullname'] + ' - ' + user['role']['description'])

    title = {
        'short_project_name': project.short_name,
        'FULL_NAME_PROJECT': project.name,
        'curator': '\n'.join(curator),
        'supervisor': '\n'.join(supervisor)
    }

    # Календарный план
    calendar_plan = []
    number = 0
    responsible = ' '

    calendar_plans = [calendar_plan.get_dto() for calendar_plan in ProjectCalendarPlan.fetch(Project.id == project_id)]
    control_user = [project_dto['fullname'] for project_dto in project_dto['users']
                    if project_dto['role']['slug'] == 'SUPERVISOR']

    # calendar_plans.sort(key=lambda x: x['start_date_plan'])
    for calendar_plan_data in calendar_plans:

        if calendar_plan_data['awaiting_result']:
            calendar_plan_results = calendar_plan_data['awaiting_result']
        else:
            calendar_plan_results = ' '

        number += 1
        for user in calendar_plan_data['users']:
            if user['role']['slug'] == 'EXECUTOR':
                responsible = user['fullname']

        calendar_plan.append({
            'number': number,
            'name': calendar_plan_data['name'],
            'start_date': datetime.datetime.strptime(calendar_plan_data['start_date_plan'], '%Y-%m-%d').strftime(
                '%d.%m.%Y') if calendar_plan_data['start_date_plan'] is not None else ' ',
            'end_date': datetime.datetime.strptime(calendar_plan_data['end_date_plan'], '%Y-%m-%d').strftime(
                '%d.%m.%Y') if calendar_plan_data['end_date_plan'] is not None else ' ',
            'result': calendar_plan_results,
            'responsible': responsible,
            'control_user': '\n'.join(control_user)
        })

    # План бюджета и закупок проекта
    budgets = {}
    budget_number = []
    count_budget = []
    number = 0
    budgets_data = [budget.get_dto() for budget in ProjectBudget.fetch(ProjectBudget.project == project_id)]
    for budget in budgets_data:
        if budget['stage']['id'] in count_budget:
            break
        else:
            count_budget.append(budget['stage']['id'])
            number += 1
            budget_number.append(number)

    budgets_data = []
    own_funds_total = []
    priority_funding_total = []
    other_funding_total = []
    total_total = []
    index = 0
    for budget_id in count_budget:
        number = budget_number[index]
        budget_calendar_plans = [budget.get_dto() for budget in ProjectBudget.fetch(ProjectBudget.stage == budget_id)]

        budgets_data.append({
            'number': number,
            'name': budget_calendar_plans[0]['stage']['name'],

            # Собственные средства УГМУ
            'wage_own_funds': sum([budget_calendar_plan['spending_costs']
                                   for budget_calendar_plan
                                   in budget_calendar_plans
                                   if budget_calendar_plan['costs_name'] == 'WAGE'
                                   and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'overheads_own_funds': sum([budget_calendar_plan['spending_costs']
                                        for budget_calendar_plan
                                        in budget_calendar_plans
                                        if budget_calendar_plan['costs_name'] == 'OVERHEADS'
                                        and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'business_trips_own_funds': sum([budget_calendar_plan['spending_costs']
                                             for budget_calendar_plan
                                             in budget_calendar_plans
                                             if budget_calendar_plan['costs_name'] == 'BUSINESS_TRIPS'
                                             and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'consumables_own_funds': sum([budget_calendar_plan['spending_costs']
                                          for budget_calendar_plan
                                          in budget_calendar_plans
                                          if budget_calendar_plan['costs_name'] == 'CONSUMABLES'
                                          and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'equipment_own_funds': sum([budget_calendar_plan['spending_costs']
                                        for budget_calendar_plan
                                        in budget_calendar_plans
                                        if budget_calendar_plan['costs_name'] == 'EQUIPMENT'
                                        and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'other_own_funds': sum([budget_calendar_plan['spending_costs']
                                    for budget_calendar_plan
                                    in budget_calendar_plans
                                    if (budget_calendar_plan['costs_name'] == 'SOFTWARE'
                                        or budget_calendar_plan['costs_name'] == 'EDUCATION')
                                    and budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),
            'own_funds_total': sum([budget_calendar_plan['spending_costs']
                                    for budget_calendar_plan
                                    in budget_calendar_plans
                                    if budget_calendar_plan['funding_source'] == 'OWN_FUNDS']),

            # Финансирование извне
            'wage_priority_funding': sum([budget_calendar_plan['spending_costs']
                                          for budget_calendar_plan
                                          in budget_calendar_plans
                                          if budget_calendar_plan['costs_name'] == 'WAGE'
                                          and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'overheads_priority_funding': sum([budget_calendar_plan['spending_costs']
                                               for budget_calendar_plan
                                               in budget_calendar_plans
                                               if budget_calendar_plan['costs_name'] == 'OVERHEADS'
                                               and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'business_trips_priority_funding': sum([budget_calendar_plan['spending_costs']
                                                    for budget_calendar_plan
                                                    in budget_calendar_plans
                                                    if budget_calendar_plan['costs_name'] == 'BUSINESS_TRIPS'
                                                    and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'consumables_priority_funding': sum([budget_calendar_plan['spending_costs']
                                                 for budget_calendar_plan
                                                 in budget_calendar_plans
                                                 if budget_calendar_plan['costs_name'] == 'CONSUMABLES'
                                                 and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'equipment_priority_funding': sum([budget_calendar_plan['spending_costs']
                                               for budget_calendar_plan
                                               in budget_calendar_plans
                                               if budget_calendar_plan['costs_name'] == 'EQUIPMENT'
                                               and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'other_priority_funding': sum([budget_calendar_plan['spending_costs']
                                           for budget_calendar_plan
                                           in budget_calendar_plans
                                           if (budget_calendar_plan['costs_name'] == 'SOFTWARE'
                                               or budget_calendar_plan['costs_name'] == 'EDUCATION')
                                           and budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),
            'priority_funding_total': sum([budget_calendar_plan['spending_costs']
                                           for budget_calendar_plan
                                           in budget_calendar_plans
                                           if budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']),

            # Иное финансирование
            'wage_other_funding': sum([budget_calendar_plan['spending_costs']
                                       for budget_calendar_plan
                                       in budget_calendar_plans
                                       if budget_calendar_plan['costs_name'] == 'WAGE'
                                       and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'overheads_other_funding': sum([budget_calendar_plan['spending_costs']
                                            for budget_calendar_plan
                                            in budget_calendar_plans
                                            if budget_calendar_plan['costs_name'] == 'OVERHEADS'
                                            and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'business_trips_other_funding': sum([budget_calendar_plan['spending_costs']
                                                 for budget_calendar_plan
                                                 in budget_calendar_plans
                                                 if budget_calendar_plan['costs_name'] == 'BUSINESS_TRIPS'
                                                 and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'consumables_other_funding': sum([budget_calendar_plan['spending_costs']
                                              for budget_calendar_plan
                                              in budget_calendar_plans
                                              if budget_calendar_plan['costs_name'] == 'CONSUMABLES'
                                              and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'equipment_other_funding': sum([budget_calendar_plan['spending_costs']
                                            for budget_calendar_plan
                                            in budget_calendar_plans
                                            if budget_calendar_plan['costs_name'] == 'EQUIPMENT'
                                            and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'other_other_funding': sum([budget_calendar_plan['spending_costs']
                                        for budget_calendar_plan
                                        in budget_calendar_plans
                                        if (budget_calendar_plan['costs_name'] == 'SOFTWARE'
                                            or budget_calendar_plan['costs_name'] == 'EDUCATION')
                                        and budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),
            'other_funding_total': sum([budget_calendar_plan['spending_costs']
                                        for budget_calendar_plan
                                        in budget_calendar_plans
                                        if budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']),

            # Всего
            'wage_total': round(sum([budget_calendar_plan['spending_costs']
                                     for budget_calendar_plan
                                     in budget_calendar_plans
                                     if budget_calendar_plan['costs_name'] == 'WAGE']), 2),
            'overheads_total': round(sum([budget_calendar_plan['spending_costs']
                                          for budget_calendar_plan
                                          in budget_calendar_plans
                                          if budget_calendar_plan['costs_name'] == 'OVERHEADS']), 2),
            'business_total': round(sum([budget_calendar_plan['spending_costs']
                                         for budget_calendar_plan
                                         in budget_calendar_plans
                                         if budget_calendar_plan['costs_name'] == 'BUSINESS_TRIPS']), 2),
            'consumables_total': round(sum([budget_calendar_plan['spending_costs']
                                            for budget_calendar_plan
                                            in budget_calendar_plans
                                            if budget_calendar_plan['costs_name'] == 'CONSUMABLES']), 2),
            'equipment_total': round(sum([budget_calendar_plan['spending_costs']
                                          for budget_calendar_plan
                                          in budget_calendar_plans
                                          if budget_calendar_plan['costs_name'] == 'EQUIPMENT']), 2),
            'other_total': round(sum([budget_calendar_plan['spending_costs']
                                      for budget_calendar_plan
                                      in budget_calendar_plans
                                      if (budget_calendar_plan['costs_name'] == 'SOFTWARE'
                                          or budget_calendar_plan['costs_name'] == 'EDUCATION')]), 2),
            'total_total': round(sum([budget_calendar_plan['spending_costs']
                                      for budget_calendar_plan
                                      in budget_calendar_plans]), 2)
        })
        own_funds_total.append(
            round(sum([budget_calendar_plan['spending_costs']
                       for budget_calendar_plan
                       in budget_calendar_plans
                       if budget_calendar_plan['funding_source'] == 'OWN_FUNDS']), 2)
        )
        priority_funding_total.append(
            round(sum([budget_calendar_plan['spending_costs']
                       for budget_calendar_plan
                       in budget_calendar_plans
                       if budget_calendar_plan['funding_source'] == 'PRIORITY_FUNDING']), 2)
        )
        other_funding_total.append(
            round(sum([budget_calendar_plan['spending_costs']
                       for budget_calendar_plan
                       in budget_calendar_plans
                       if budget_calendar_plan['funding_source'] == 'OTHER_FUNDING']), 2)
        )
        total_total.append(
            round(sum([budget_calendar_plan['spending_costs']
                       for budget_calendar_plan
                       in budget_calendar_plans]), 2)
        )
        index += 1

        budgets = {
            'budgets': budgets_data,
            'own_funds_total': round(sum(own_funds_total), 2),
            'priority_funding_total': round(sum(priority_funding_total), 2),
            'other_funding_total': round(sum(other_funding_total), 2),
            'total_total': round(sum(total_total), 2)
        }

    document_data = title | {'calendar_plan': calendar_plan} | budgets
    document.render(document_data)

    file_stream = io.BytesIO()
    document.save(file_stream)
    file_stream.seek(0)

    return file_stream, project.name
