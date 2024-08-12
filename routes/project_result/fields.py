from webargs import fields

create_result_model = {
    'project_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'units_measure': fields.String(required=True),
    'characteristic': fields.String(required=True),
    'approval_doc': fields.String(required=False),
}

edit_result_model = {
    'result_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'units_measure': fields.String(required=True),
    'characteristic': fields.String(required=True),
    'approval_doc': fields.String(required=False),
    'status': fields.String(required=False),
}

set_result_user_role_model = {
    'user_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True),
    'project_result_id': fields.Integer(required=True)
}

remove_result_model = {
    'result_id': fields.Integer(required=True)
}

remove_result_value_model = {
    'value_id': fields.Integer(required=True)
}

result_value_model = {
    'result_id': fields.Integer(required=True),
    'achievement_date': fields.Date(required=True),
    'plan_value': fields.Integer(required=True),
    'forecast_value': fields.Integer(required=False)
}

result_value_update_model = {
    'value_id': fields.Integer(required=True),
    'achievement_date': fields.Date(required=True),
    'plan_value': fields.Integer(required=True),
    'forecast_value': fields.Integer(required=False)
}
