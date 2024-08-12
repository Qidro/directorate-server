from models.log import ProjectLog
from datetime import datetime
from constants.constants import project_status_list
from constants.constants_log import project_dict


def project_log(
        author_id: int,
        author_name: str,
        project_dto: dict,
        action: str,
        prev_project_dto: dict = None
):
    match action:
        case 'CREATE_PROJECT':
            message = f'{author_name} создал проект из проектного предложения'
            new_status = 'INITIATION'
        case 'UPDATE_PROJECT':
            changed_fields = []
            for field in prev_project_dto:
                if prev_project_dto[field] != project_dto[field]:
                    changed_fields.append(project_dict[field])

            if not changed_fields:
                return

            message = f'{author_name} изменил поля проекта: {", ".join(changed_fields)}'
        case _:
            return

    ProjectLog(
        project=project_dto['id'],
        action=action,
        new_status=new_status,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def project_role_log(
        author_id: int,
        author_name: str,
        project_id: int,
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

    ProjectLog(
        project=project_id,
        action=action,
        user_change=author_id,
        date_change=datetime.utcnow(),
        message=message
    ).save()


def project_stage_log(
        author_id: int,
        author_name: str,
        project_id: int,
        new_status: str
):
    actions = ProjectLog.fetch((ProjectLog.project == project_id) &
                     ((ProjectLog.action == 'CREATE_PROJECT') | (ProjectLog.action == 'UPDATE_STAGE')))
    last_action = actions[len(actions) - 1]

    last_action.date_change_out = datetime.utcnow()
    last_action.save()

    ProjectLog(
        project=project_id,
        action='UPDATE_STAGE',
        new_status=new_status,
        user_change=author_id,
        message=f'{author_name} изменил стадию проекта',
        date_change=datetime.utcnow()
    ).save()


def project_file_log(
        author_id: int,
        author_name: str,
        project_id: int,
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

    ProjectLog(
        project=project_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def get_project_logs(project_id: int, position: int):
    logs = ProjectLog.fetch(
        condition=ProjectLog.project == project_id,
        order_by=ProjectLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
