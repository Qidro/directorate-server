from models.log import UserLog
from datetime import datetime
from constants.constants_log import user_dict


def user_log(
        author_id: int,
        author_name: str,
        user_dto: dict,
        action: str,
        prev_user_dto: dict = None
):
    match action:
        case 'UPDATE_USER':
            changed_fields = []
            prev_user_dto.pop('fullname')
            for field in prev_user_dto:
                if prev_user_dto[field] != user_dto[field]:
                    changed_fields.append(user_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил данные пользователя: {", ".join(changed_fields)}'
        case _:
            return

    UserLog(
        user=user_dto['id'],
        user_change=author_id,
        date_change=datetime.utcnow(),
        action=action,
        message=message,
    ).save()


def user_right_log(
        author_id: int,
        author_name: str,
        user_right_dto: dict,
        action: str,
):
    match action:
        case 'SET_RIGHT':
            message = f'{author_name} добавил пользователю право "{user_right_dto["right"]["name"]}"'
        case 'REMOVE_RIGHT':
            message = f'{author_name} удалил у пользователя право "{user_right_dto["right"]["name"]}"'
        case _:
            return

    UserLog(
        user=user_right_dto['user']['id'],
        user_change=author_id,
        date_change=datetime.utcnow(),
        action=action,
        message=message,
    ).save()


def get_user_logs(user_id: int, position: int):
    logs = UserLog.fetch(
        condition=UserLog.user == user_id,
        order_by=UserLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
