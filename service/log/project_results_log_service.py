from models.log import ProjectLog, ProjectResultsLog
from datetime import datetime
from constants.constants_log import result_dict, result_dict_values_dict


def result_log(
        author_id: int,
        author_name: str,
        result_dto: dict,
        action: str,
        prev_result_dto: dict = None
):
    match action:
        case 'CREATE_RESULT':
            message = f'{author_name} создал новый результат "{result_dto["name"]}"'
        case 'DELETE_RESULT':
            message = f'{author_name} удалил результат "{result_dto["name"]}"'
        case 'UPDATE_RESULT':
            changed_fields = []
            for field in prev_result_dto:
                if prev_result_dto[field] != result_dto[field]:
                    changed_fields.append(result_dict[field])

            if changed_fields:
                ProjectResultsLog(
                    result=result_dto['id'],
                    action=action,
                    user_change=author_id,
                    message=f'{author_name} изменил поля результата: {", ".join(changed_fields)}',
                    date_change=datetime.utcnow()
                ).save()

            return
        case _:
            return

    ProjectLog(
        project=result_dto['project']['id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def result_role_log(
        author_id: int,
        author_name: str,
        result_id: int,
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

    ProjectResultsLog(
        result=result_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def value_log(
        author_id: int,
        author_name: str,
        value_dto: dict,
        action: str,
        prev_value_dto: dict = None
):
    match action:
        case 'CREATE_VALUE':
            message = f'{author_name} создал новое значение в бюджете'
        case 'DELETE_VALUE':
            message = f'{author_name} удалил значение в бюджете'
        case 'UPDATE_VALUE':
            changed_fields = []
            for field in prev_value_dto:
                if prev_value_dto[field] != value_dto[field]:
                    changed_fields.append(result_dict_values_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля значения бюджета: {", ".join(changed_fields)}'
        case _:
            return

    ProjectResultsLog(
        result=value_dto['result']['id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def get_results_logs(result_id: int, position: int):
    logs = ProjectResultsLog.fetch(
        condition=ProjectResultsLog.result == result_id,
        order_by=ProjectResultsLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
