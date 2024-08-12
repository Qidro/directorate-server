from datetime import datetime
from constants.constants_log import indicator_dict, indicator_value_dict
from models import ProjectLog, ProjectIndicatorsLog


def indicator_log(
        author_id: int,
        author_name: str,
        indicator_dto: dict,
        action: str,
        prev_indicator_dto: dict = None
):
    match action:
        case 'CREATE_INDICATOR':
            message = f'{author_name} создал новый индикатор "{indicator_dto["name"]}"'
        case 'DELETE_INDICATOR':
            message = f'{author_name} удалил индикатор "{indicator_dto["name"]}"'
        case 'UPDATE_INDICATOR':
            changed_fields = []
            for field in prev_indicator_dto:
                if prev_indicator_dto[field] != indicator_dto[field]:
                    changed_fields.append(indicator_dict[field])

            if changed_fields:
                ProjectIndicatorsLog(
                    indicator=indicator_dto['id'],
                    action=action,
                    user_change=author_id,
                    message=f'{author_name} изменил поля индикатора: {", ".join(changed_fields)}',
                    date_change=datetime.utcnow()
                ).save()

            return
        case _:
            return

    ProjectLog(
        project=indicator_dto['project']['id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def indicator_role_log(
        author_id: int,
        author_name: str,
        indicator_id: int,
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

    ProjectIndicatorsLog(
        indicator=indicator_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def indicator_values_log(
        author_id: int,
        author_name: str,
        value_dto: dict,
        action: str,
        prev_value_dto: dict = None
):
    match action:
        case 'CREATE_VALUE':
            message = f'{author_name} создал новое значение в индикаторе'
        case 'DELETE_VALUE':
            message = f'{author_name} удалил значение в индикаторе'
        case 'UPDATE_VALUE':
            changed_fields = []
            for field in prev_value_dto:
                if prev_value_dto[field] != value_dto[field]:
                    changed_fields.append(indicator_value_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля значения индикатора: {", ".join(changed_fields)}'
        case _:
            return

    ProjectIndicatorsLog(
        indicator=value_dto['indicator']['id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def get_indicator_logs(indicator_id: int, position: int):
    logs = ProjectIndicatorsLog.fetch(
        condition=ProjectIndicatorsLog.indicator == indicator_id,
        order_by=ProjectIndicatorsLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
