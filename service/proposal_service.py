from models import Proposal, User, ProposalComment, ProposalExperts, ProposalVerdicts, UserRight, Right
from exceptions import ApiError
from constants.constants import final_proposal_verdict_list, expert_verdict_list
import datetime
from service import send_mail_service


# Создание ПП
def create(user_id: int, name: str, realization_period_start: datetime.date, realization_period_end: datetime.date,
           executors: str, justification: str, purpose: str, results: str, target_indicators: str,
           planned_actions: str, resources: str, contacts: str):

    current_date = datetime.date.today()

    project_proposal = Proposal(
        user=user_id,
        status='REVIEW',
        submission_date=current_date,
        name=name,
        realization_period_start=realization_period_start,
        realization_period_end=realization_period_end,
        executors=executors,
        justification=justification,
        purpose=purpose,
        results=results,
        target_indicators=target_indicators,
        planned_actions=planned_actions,
        resources=resources,
        contacts=contacts,
    )
    project_proposal.save()

    proposal = Proposal.fetch(Proposal.id == project_proposal)[0]

    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')
    directors = User.select().join(UserRight).join(Right).where(Right.slug == 'DIRECTOR-EX')

    connect = send_mail_service.create_smtp_connect()
    for director in directors:
        send_mail_service.send_email(
            connect, director.email, 'Уведомление!',
            f'{user.firstname} {user.surname} подал проектное предложение {proposal.name} на рассмотрение'
        )
    connect.quit()

    return proposal.get_dto()


def update(proposal_id: int, user_id: int, name: str, realization_period_start: datetime.date,
           realization_period_end: datetime.date, executors: str, justification: str, purpose: str, results: str,
           target_indicators: str, planned_actions: str, resources: str, contacts: str):

    project_proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not project_proposal:
        raise ApiError.BadRequest('Proposal not found')

    if project_proposal.status != 'REJECT':
        raise ApiError.BadRequest('Proposal no status reject')

    prev_proposal_data = Proposal.fetch(Proposal.id == proposal_id)[0].get_dto()

    project_proposal = Proposal.update(
        user=user_id,
        status='EXPERTS_EVALUATE',
        name=name,
        realization_period_start=realization_period_start,
        realization_period_end=realization_period_end,
        executors=executors,
        justification=justification,
        purpose=purpose,
        results=results,
        target_indicators=target_indicators,
        planned_actions=planned_actions,
        resources=resources,
        contacts=contacts,
    ).where(Proposal.id == proposal_id)
    project_proposal.execute()

    verdict = ProposalVerdicts.update(status='', date=None).where(ProposalVerdicts.project_proposal == proposal_id)
    verdict.execute()

    new_proposal_data = Proposal.fetch(Proposal.id == proposal_id)[0].get_dto()

    return new_proposal_data, prev_proposal_data


# Получение ПП где user является инициатором
def get_my(user_id: int):
    proposals = Proposal.fetch(Proposal.user_id == user_id)
    return [proposal.get_dto() for proposal in proposals if proposal.isArchived == False]


# Получение всех ПП
def get_all():
    proposals = Proposal.fetch()
    return [proposal.get_dto() for proposal in proposals if proposal.isArchived == False]


# Получение ПП где user является экспертом
def get_when_expert(user_id: int):
    proposals_id = [proposal_experts.project_proposal for proposal_experts in ProposalExperts.select().where(ProposalExperts.user_id == user_id)]
    proposals = Proposal.fetch(Proposal.id << proposals_id)
    return [proposal.get_dto() for proposal in proposals if proposal.isArchived == False]


# Получение данных ПП
def get_proposal(proposal_id):
    proposal = Proposal.fetch(Proposal.id == proposal_id)
    if len(proposal) == 0:
        raise ApiError.BadRequest("Proposal not found")

    experts = [expert.get_dto() for expert in
               ProposalExperts.select().where(ProposalExperts.project_proposal == proposal_id)]

    project_comment = [comment.get_dto() for comment in
                       ProposalComment.select().where(ProposalComment.proposal_id == proposal_id)]

    verdict = ProposalVerdicts.get_or_none(ProposalVerdicts.project_proposal == proposal_id)
    if verdict:
        verdict = verdict.get_dto()

    return {**proposal[0].get_dto(), 'comments': project_comment, 'experts': experts, 'verdict': verdict}


# Назначение экспертов на ПП
def set_expert(proposal_id: int, user_id: int, current_user_id: int):
    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    current_user = User.get_or_none(User.id == current_user_id)
    if not current_user:
        raise ApiError.BadRequest('Current user not found')

    current_date = datetime.date.today()

    appointed_experts = ProposalExperts.select().where(ProposalExperts.project_proposal == proposal_id)
    if len(appointed_experts) == 0:
        proposal = Proposal.update(status='EXPERTS_EVALUATE').where(Proposal.id == proposal_id)
        proposal.execute()

    appointed_experts = ProposalExperts(
        project_proposal=proposal_id,
        user=user,
        director=current_user_id,
        date_appointment=current_date
    )
    appointed_experts.save()

    connect = send_mail_service.create_smtp_connect()
    send_mail_service.send_email(
        connect, user.email, 'Уведомление !',
        f'{user.firstname} {user.surname} Вас назначили экспертом на проектное предложение {proposal.name}'
    )
    connect.quit()

    return appointed_experts.get_dto()


def remove_expert(proposal_id: int, user_id: int):
    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    expert = ProposalExperts.get_or_none(ProposalExperts.project_proposal == proposal_id, ProposalExperts.user == user_id)
    if not expert:
        return

    ProposalExperts.delete().where(ProposalExperts.id == expert).execute()

    appointed_experts = ProposalExperts.select().where(ProposalExperts.project_proposal == proposal_id)
    if len(appointed_experts) == 0:
        proposal = Proposal.update(status='REVIEW').where(Proposal.id == proposal_id)
        proposal.execute()

    return expert.get_dto()


# Вынесение финального вердикта
def set_verdict(proposal_id: int, user, conclusion: str, status: str):
    current_date = datetime.date.today()

    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    if status not in final_proposal_verdict_list:
        ApiError.BadRequest('Verdict not found')

    verdict_manager = ProposalVerdicts.delete().where(ProposalVerdicts.project_proposal == proposal)
    verdict_manager.execute()

    verdict_manager = ProposalVerdicts(
        project_proposal=proposal,
        user=user,
        conclusion=conclusion,
        status=status,
        date=current_date
    )
    verdict_manager.save()

    project_proposal = Proposal.update(status=status).where(Proposal.id == proposal_id)
    project_proposal.execute()

    if status == 'REJECT':
        expert_status = ProposalExperts.update(verification_status='', date_verification=None,
                                               date_appointment=datetime.date.today())\
            .where(ProposalExperts.project_proposal == proposal_id)
        expert_status.execute()

    return verdict_manager.get_dto()


# Добавление комментариев Экспертом
def add_comment(proposal_id: int, user_id: int, status: str, name: str, realization_period: str, executors: str,
                justification: str, purpose: str, results: str, target_indicators: str,
                planned_actions: str, resources: str, contacts: str):

    proposal = Proposal.get_or_none(Proposal.id == proposal_id)
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    if status not in expert_verdict_list:
        ApiError.BadRequest('Status not found')

    current_date = datetime.date.today()

    project_comment = ProposalComment.delete().where(ProposalComment.proposal == proposal_id,
                                                    ProposalComment.user == user_id)
    project_comment.execute()

    project_comment = ProposalComment(
        proposal=proposal,
        user=user_id,
        date=current_date,
        name=name,
        realization_period=realization_period,
        executors=executors,
        justification=justification,
        purpose=purpose,
        results=results,
        target_indicators=target_indicators,
        planned_actions=planned_actions,
        resources=resources,
        contacts=contacts
    )
    project_comment.save()

    appointed_experts = ProposalExperts.update(verification_status=status, date_verification=current_date)\
        .where(ProposalExperts.user == user_id, ProposalExperts.project_proposal == proposal_id)
    appointed_experts.execute()

    experts = ProposalExperts.select()\
        .where(ProposalExperts.project_proposal == proposal_id)

    is_experts_checked = False
    for expert in experts:
        if expert.verification_status not in expert_verdict_list:
            is_experts_checked = False
            break
        else:
            is_experts_checked = True

    if is_experts_checked:
        proposal = Proposal.update(status='DIRECTOR_EVALUATE').where(Proposal.id == proposal_id)
        proposal.execute()

    return ProposalComment.select().where(ProposalComment.id == project_comment)[0].get_dto()


def get_experts(proposal_id: int):
    proposal = Proposal.fetch(Proposal.id == proposal_id)
    if len(proposal) == 0:
        raise ApiError.BadRequest('Proposal not found')

    appointed_experts = [expert['user_id'] for expert in proposal[0].get_dto()['experts']]

    users = User.fetch(condition=User.id.not_in(appointed_experts))
    experts = [user.get_dto() for user in users if any(user_right.right.slug == 'EXPERT-EX' for user_right in user.rights) and user.id != proposal[0].user.id]
    return experts
