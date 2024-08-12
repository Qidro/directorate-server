from datetime import datetime
from models.log import BackpackLog
from constants.constants_log import backpack_dict


def backpack_log(
        author_id: int,
        author_name: str,
        backpack_dto: dict,
        action: str,
        prev_backpack_dto: dict = None
):
    match action:
        case 'UPDATE_BACKPACK':
            changed_fields = []
            prev_backpack_dto.pop('change_date', None)
            for field in prev_backpack_dto:
                if prev_backpack_dto[field] != backpack_dto[field]:
                    changed_fields.append(backpack_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля портфеля: {", ".join(changed_fields)}'
        case _:
            return

    BackpackLog(
        backpack=backpack_dto['id'],
        action=action,
        user_change=author_id,
        date_change=datetime.utcnow(),
        message=message
    ).save()


def backpack_role_log(
        author_id: int,
        author_name: str,
        backpack_id: int,
        user_role_dto: dict,
        action: str
):
    match action:
        case 'SET_ROLE':
            message = f'{author_name} назначил пользователя {user_role_dto["fullname"]} на роль "{user_role_dto["role"]["name"]}"'
        case 'REMOVE_ROLE':
            message = f'{author_name} снял пользователя {user_role_dto["fullname"]} с роли "{user_role_dto["role"]["name"]}"'
        case _:
            return

    BackpackLog(
        backpack=backpack_id,
        action=action,
        user_change=author_id,
        date_change=datetime.utcnow(),
        message=message
    ).save()


def backpack_file_log(
        author_id: int,
        author_name: str,
        backpack_id: int,
        file_dto: dict,
        action: str
):
    match action:
        case 'UPLOAD_FILE':
            message = f'{author_name} загрузил документ "{file_dto["filename"]}"'
        case 'REMOVE_FILE':
            message = f'{author_name} удалил документ "{file_dto["filename"]}"'
        case _:
            return

    BackpackLog(
        backpack=backpack_id,
        action=action,
        user_change=author_id,
        date_change=datetime.utcnow(),
        message=message
    ).save()


def get_backpack_logs(backpack_id: int, position: int):
    logs = BackpackLog.fetch(
        condition=BackpackLog.backpack == backpack_id,
        order_by=BackpackLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
