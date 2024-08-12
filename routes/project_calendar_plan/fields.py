from webargs import fields

create_stage_model = {
    'project_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'awaiting_result': fields.String(required=True)
}

update_stage_model = {
    'calendar_plan_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'awaiting_result': fields.String(required=True)
}

create_work_model = {
    'project_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'awaiting_result': fields.String(required=True),
    'start_date_plan': fields.Date(required=True),
    'start_date_forecast': fields.Date(required=False, load_default=None),
    'start_date_fact': fields.Date(required=False, load_default=None),
    'end_date_plan': fields.Date(required=True),
    'end_date_forecast': fields.Date(required=False, load_default=None),
    'end_date_fact': fields.Date(required=False, load_default=None),
    'executor_id': fields.Integer(required=True),
    'approval_doc': fields.String(required=True),
    'parent_stage_id': fields.Integer(required=True)
}

create_point_model = {
    'project_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'end_date_plan': fields.Date(required=True),
    'end_date_forecast': fields.Date(required=True),
    'end_date_fact': fields.Date(required=True),
    'executor_id': fields.Integer(required=True),
    'approval_doc': fields.String(required=True),
}

update_work_model = {
    'calendar_plan_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'awaiting_result': fields.String(required=True),
    'start_date_plan': fields.Date(required=True),
    'start_date_forecast': fields.Date(required=False, load_default=None),
    'start_date_fact': fields.Date(required=False, load_default=None),
    'end_date_plan': fields.Date(required=True),
    'end_date_forecast': fields.Date(required=False, load_default=None),
    'end_date_fact': fields.Date(required=False, load_default=None),
    'approval_doc': fields.String(required=True),
    'parent_stage_id': fields.Integer(required=True)
}

update_point_model = {
    'calendar_plan_id': fields.Integer(required=True),
    'type': fields.String(required=True),
    'name': fields.String(required=True),
    'end_date_plan': fields.Date(required=True),
    'end_date_forecast': fields.Date(required=True),
    'end_date_fact': fields.Date(required=True),
    'approval_doc': fields.String(required=True),
}

delete_model = {
    'calendar_plan_id': fields.Integer(required=True)
}

add_calendar_plan_result_model = {
    'calendar_plan_id': fields.Integer(required=True),
    'result_id': fields.Integer(required=True)
}

remove_calendar_plan_result_model = {
    **add_calendar_plan_result_model
}

set_user_role_model = {
    'user_id': fields.Integer(required=True),
    'calendar_plan_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True)
}

update_status_model = {
    'calendar_plan_id': fields.Integer(required=True),
    'status':  fields.String(required=True)
}
