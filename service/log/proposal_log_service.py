from models.log import ProposalLog
from datetime import datetime
from constants.constants_log import proposal_dict


def proposal_log(
        author_id: int,
        author_name: str,
        proposal_dto: dict,
        action: str,
        prev_proposal_dto: dict = None
):
    match action:
        case 'UPDATE_PROPOSAL':
            changed_fields = []
            prev_proposal_dto.pop('status', None)
            for field in prev_proposal_dto:
                if prev_proposal_dto[field] != proposal_dto[field]:
                    changed_fields.append(proposal_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля проектного предложения: {", ".join(changed_fields)}'
        case _:
            return

    ProposalLog(
        proposal=proposal_dto['id'],
        user_change=author_id,
        message=message,
        action=action,
        date_change=datetime.utcnow()
    ).save()


def proposal_comment_log(
        author_id: int,
        author_name: str,
        proposal_id: int
):
    ProposalLog(
        proposal=proposal_id,
        user_change=author_id,
        message=f'Эксперт {author_name} оставил комментарий',
        action='ADD_COMMENT',
        date_change=datetime.utcnow()
    ).save()


def proposal_expert_log(
        author_id: int,
        author_name: str,
        proposal_id: int,
        expert_dto: dict,
        action: str
):
    match action:
        case 'SET_EXPERT':
            message = f'{author_name} назначит эксперта {expert_dto["user"]["fullname"]}'
        case 'REMOVE_EXPERT':
            message = f'{author_name} удалил эксперта {expert_dto["user"]["fullname"]}'
        case _:
            return

    ProposalLog(
        proposal=proposal_id,
        user_change=author_id,
        message=message,
        action=action,
        date_change=datetime.utcnow()
    ).save()


def get_proposal_logs(proposal_id: int, position: int):
    logs = ProposalLog.fetch(
        condition=ProposalLog.proposal == proposal_id,
        order_by=ProposalLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
