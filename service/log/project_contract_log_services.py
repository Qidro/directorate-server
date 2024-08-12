from models.log import ProjectLog, ProjectContractsLog
from datetime import datetime
from constants.constants_log import contract_dict


def contract_log(
        author_id: int,
        author_name: str,
        contract_dto: dict,
        action: str,
        prev_contract_dto: dict = None
):
    match action:
        case 'CREATE_CONTRACT':
            message = f'{author_name} создал новый контракт "{contract_dto["name"]}"'
        case 'DELETE_CONTRACT':
            message = f'{author_name} удалил контракт "{contract_dto["name"]}"'
        case 'UPDATE_CONTRACT':
            changed_fields = []
            for field in prev_contract_dto:
                if prev_contract_dto[field] != contract_dto[field]:
                    changed_fields.append(contract_dict[field])

            if changed_fields:
                ProjectContractsLog(
                    contract=contract_dto['id'],
                    action=action,
                    user_change=author_id,
                    message=f'{author_name} изменил поля контракта: {", ".join(changed_fields)}',
                    date_change=datetime.utcnow()
                ).save()

            return
        case _:
            return

    ProjectLog(
        project=contract_dto['project']['id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def contract_role_log(
        author_id: int,
        author_name: str,
        contract_id: int,
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

    ProjectContractsLog(
        contract=contract_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def contract_file_log(
        author_id: int,
        author_name: str,
        contract_id: int,
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

    ProjectContractsLog(
        contract=contract_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def contract_stage_log(
        author_id: int,
        author_name: str,
        contract_id: int,
):
    ProjectContractsLog(
        contract=contract_id,
        action='UPDATE_STAGE',
        user_change=author_id,
        message=f'{author_name} изменил стадию контракта',
        date_change=datetime.utcnow()
    ).save()


def get_contract_logs(contract_id: int, position: int):
    logs = ProjectContractsLog.fetch(
        condition=ProjectContractsLog.contract == contract_id,
        order_by=ProjectContractsLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
