from models.log import ProjectLog
from datetime import datetime
from constants.constants_log import budget_dict


def budget_log(
        author_id: int,
        author_name: str,
        budget_dto: dict,
        action: str,
        prev_budget_dto: dict = None
):
    match action:
        case 'CREATE_BUDGET':
            message = f'{author_name} создал новый бюджет'
        case 'DELETE_BUDGET':
            message = f'{author_name} удалил бюджет'
        case 'UPDATE_BUDGET':
            changed_fields = []
            for field in prev_budget_dto:
                if prev_budget_dto[field] != budget_dto[field]:
                    changed_fields.append(budget_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля бюджета: {", ".join(changed_fields)}'
        case _:
            return

    ProjectLog(
        project=budget_dto['project_id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()
