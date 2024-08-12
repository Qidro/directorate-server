from models import User, ProjectCalendarPlan, ProjectCalendarPlanRole, ProjectResults, Project
from models.log import ProjectLog, ProjectCalendarPlanLog
from datetime import datetime
from constants.constants_log import calendar_plan_work_dict

type_names = {
    'WORK': 'работу',
    'STAGE': 'этап',
    'CONTROL_POINT': 'контрольную точку'
}

type_names_genitive = {
    'WORK': 'работы',
    'STAGE': 'этапа',
    'CONTROL_POINT': 'контрольной точки'
}


def calendar_plan_log(
        author_id: int,
        author_name: str,
        cp_dto: dict,
        action: str,
        prev_cp_dto: dict = None
):
    type_name = type_names.get(cp_dto['type'], 'контрольную точку')

    match action:
        case 'CREATE':
            message = f'{author_name} создал {type_name} "{cp_dto["name"]}"'
        case 'DELETE':
            message = f'{author_name} удалил {type_name} "{cp_dto["name"]}"'
        case 'UPDATE':
            changed_fields = []
            prev_cp_dto.pop('status', None)
            for field in prev_cp_dto:
                if prev_cp_dto[field] != cp_dto[field]:
                    changed_fields.append(calendar_plan_work_dict[field])

            if changed_fields:
                type_name = type_names_genitive.get(cp_dto['type'], 'контрольной точки')
                ProjectCalendarPlanLog(
                    calendar_plan=cp_dto['id'],
                    action=f'{action}_{cp_dto["type"]}',
                    user_change=author_id,
                    message=f'{author_name} изменил поля {type_name}: {", ".join(changed_fields)}',
                    date_change=datetime.utcnow()
                ).save()

            return
        case _:
            return

    ProjectLog(
        project=cp_dto['project']['id'],
        action=f'{action}_{cp_dto["type"]}',
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def calendar_plan_role_log(
        author_id: int,
        author_name: str,
        cp_id: int,
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

    ProjectCalendarPlanLog(
        calendar_plan=cp_id,
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def calendar_plan_result_log(
        author_id: int,
        author_name: str,
        result_dto: dict,
        action: str
):
    match action:
        case 'ADD_RESULT':
            message = f'{author_name} добавил результат "{result_dto["result"]["name"]}"'
        case 'REMOVE_RESULT':
            message = f'{author_name} удалил результат "{result_dto["result"]["name"]}"'
        case _:
            return

    ProjectCalendarPlanLog(
        calendar_plan=result_dto['calendar_plan_id'],
        action=action,
        user_change=author_id,
        message=message,
        date_change=datetime.utcnow()
    ).save()


def get_calendar_plan_logs(calendar_plan_id: int, position: int):
    logs = ProjectCalendarPlanLog.fetch(
        condition=ProjectCalendarPlanLog.calendar_plan == calendar_plan_id,
        order_by=ProjectCalendarPlanLog.id.desc(),
        offset=position,
        limit=20
    )

    return [log.get_dto() for log in logs]
