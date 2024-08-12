from flask import Blueprint, request, jsonify, Response
from webargs import flaskparser
from decorators import login_required
from .fields import create_work_model, create_point_model, update_work_model, update_point_model, delete_model, \
    add_calendar_plan_result_model, remove_calendar_plan_result_model, set_user_role_model, update_status_model, \
    create_stage_model, update_stage_model
from service import project_calendar_plan_service
from service.log import project_calendar_plan_log_service

project_calendar_plan_router = Blueprint('project_calendar_plan', __name__)


@project_calendar_plan_router.post('/project/calendar_plan/stage/create')
@login_required
def create_stage(user):
    data = flaskparser.parser.parse(create_stage_model, request)
    calendar_plan_data = project_calendar_plan_service.create_stage(data['project_id'], data['type'], data['name'],
                                                                    data['awaiting_result'])

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=calendar_plan_data,
        action='CREATE'
    )

    return jsonify(calendar_plan_data)


@project_calendar_plan_router.post('/project/calendar_plan/work/create')
@login_required
def create_work(user):
    data = flaskparser.parser.parse(create_work_model, request)
    calendar_plan_data = project_calendar_plan_service.create_work(
        data['project_id'], data['type'], data['name'], data['awaiting_result'], data['start_date_plan'], data['start_date_forecast'],
        data['start_date_fact'], data['end_date_plan'], data['end_date_forecast'], data['end_date_fact'],
        data['executor_id'], data['approval_doc'], data['parent_stage_id']
    )

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=calendar_plan_data,
        action='CREATE'
    )

    return jsonify(calendar_plan_data)


@project_calendar_plan_router.post('/project/calendar_plan/point/create')
@login_required
def create_point(user):
    data = flaskparser.parser.parse(create_point_model, request)
    calendar_plan_data = project_calendar_plan_service.create_point(
        data['project_id'], data['type'], data['name'], data['end_date_plan'], data['end_date_forecast'],
        data['end_date_fact'], data['executor_id'], data['approval_doc'])

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=calendar_plan_data,
        action='CREATE'
    )

    return jsonify(calendar_plan_data)


@project_calendar_plan_router.post('/project/calendar_plan/work/update')
@login_required
def update_work(user):
    data = flaskparser.parser.parse(update_work_model, request)
    cp, prev_cp = project_calendar_plan_service.update_work(
        data['calendar_plan_id'], data['type'], data['name'], data['awaiting_result'], data['start_date_plan'], data['start_date_forecast'],
        data['start_date_fact'], data['end_date_plan'], data['end_date_forecast'], data['end_date_fact'],
        data['approval_doc'], data['parent_stage_id']
    )

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=cp,
        prev_cp_dto=prev_cp,
        action='UPDATE'
    )

    return jsonify(cp)


@project_calendar_plan_router.post('/project/calendar_plan/point/update')
@login_required
def update_point(user):
    data = flaskparser.parser.parse(update_point_model, request)
    cp, prev_cp = project_calendar_plan_service.update_point(
        data['calendar_plan_id'], data['name'], data['end_date_plan'], data['end_date_forecast'],
        data['end_date_fact'], data['approval_doc'])

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=cp,
        prev_cp_dto=prev_cp,
        action='UPDATE'
    )

    return jsonify(cp)


@project_calendar_plan_router.post('/project/calendar_plan/stage/update')
@login_required
def update_stage(user):
    data = flaskparser.parser.parse(update_stage_model, request)
    cp, prev_cp = project_calendar_plan_service.update_stage(data['calendar_plan_id'], data['name'], data['awaiting_result'])

    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=cp,
        prev_cp_dto=prev_cp,
        action='UPDATE'
    )

    return jsonify(cp)


@project_calendar_plan_router.get('/project/<int:project_id>/calendar_plan/stages')
@login_required
def get_stages(user, project_id):
    project_calendar_plan_stages = project_calendar_plan_service.get_stages(project_id)
    return jsonify(project_calendar_plan_stages)


@project_calendar_plan_router.get('/project/<int:project_id>/calendar_plans')
@login_required
def get_calendar_plans(user, project_id):
    all_calendar_plan = project_calendar_plan_service.get_calendar_plans(project_id)
    return jsonify(all_calendar_plan)


@project_calendar_plan_router.get('/project/calendar_plan/<int:calendar_plan_id>')
@login_required
def get_calendar_plan(user, calendar_plan_id):
    calendar_plan = project_calendar_plan_service.get_calendar_plan(calendar_plan_id)
    return jsonify(calendar_plan)


@project_calendar_plan_router.post('/project/calendar_plan/result/add')
@login_required
def add_result(user):
    data = flaskparser.parser.parse(add_calendar_plan_result_model, request)
    calendar_plan_result = project_calendar_plan_service.add_result(data['calendar_plan_id'], data['result_id'])

    project_calendar_plan_log_service.calendar_plan_result_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        result_dto=calendar_plan_result,
        action='ADD_RESULT'
    )

    return jsonify(calendar_plan_result)


@project_calendar_plan_router.delete('/project/calendar_plan/result/remove')
@login_required
def remove_result(user):
    data = flaskparser.parser.parse(remove_calendar_plan_result_model, request)
    removed_result = project_calendar_plan_service.remove_result(data['calendar_plan_id'], data['result_id'])

    project_calendar_plan_log_service.calendar_plan_result_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        result_dto=removed_result,
        action='REMOVE_RESULT'
    )

    return Response(status=204)


@project_calendar_plan_router.delete('/project/calendar_plan/delete')
@login_required
def delete(user):
    data = flaskparser.parser.parse(delete_model, request)
    cp = project_calendar_plan_service.get_calendar_plan(data['calendar_plan_id'])
    project_calendar_plan_log_service.calendar_plan_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_dto=cp,
        action='DELETE'
    )

    project_calendar_plan_service.delete(data['calendar_plan_id'])
    return Response(status=204)


@project_calendar_plan_router.get('/project/calendar_plan/cp')
@login_required
def get_cp(user):
    calendar_plan_cp = project_calendar_plan_service.get_cp()
    return jsonify(calendar_plan_cp)


@project_calendar_plan_router.get('/project/calendar_plan/roles')
@login_required
def get_roles(user):
    roles = project_calendar_plan_service.get_roles()
    return jsonify(roles)


@project_calendar_plan_router.post('/project/calendar_plan/user/role/add')
@login_required
def set_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_calendar_plan_service.set_user_role(data['user_id'], data['calendar_plan_id'],
                                                                     data['role_id'])

    project_calendar_plan_log_service.calendar_plan_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_id=data['calendar_plan_id'],
        user_role_dto=user_role,
        action='SET_ROLE'
    )

    return jsonify(user_role)


@project_calendar_plan_router.delete('/project/calendar_plan/user/role/remove')
@login_required
def remove_user_role(user):
    data = flaskparser.parser.parse(set_user_role_model, request)
    user_role = project_calendar_plan_service.remove_user_role(data['user_id'], data['calendar_plan_id'], data['role_id'])

    project_calendar_plan_log_service.calendar_plan_role_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        cp_id=data['calendar_plan_id'],
        user_role_dto=user_role,
        action='REMOVE_ROLE'
    )

    return Response(status=204)


@project_calendar_plan_router.post('/project/calendar_plan/status/update')
@login_required
def update_status(user):
    data = flaskparser.parser.parse(update_status_model, request)
    project_calendar_plan = project_calendar_plan_service.update_status(data['calendar_plan_id'], data['status'])
    return jsonify(project_calendar_plan)


@project_calendar_plan_router.get('/project/calendar_plan/<int:calendar_plan_id>/logs&position=<int:position>')
@login_required
def get_cp_logs(user, calendar_plan_id, position):
    logs = project_calendar_plan_log_service.get_calendar_plan_logs(calendar_plan_id, position)
    return jsonify(logs)
