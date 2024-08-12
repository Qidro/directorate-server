from webargs import fields

create_model = {
    'proposal_id': fields.Integer(required=True),
    'backpack_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True),
    'user_curator_id': fields.Integer(required=True)
}

delete_model = {
    'id': fields.Integer(required=True)
}

update_model = {
    'project_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'short_name': fields.String(required=True),
    'priority': fields.String(required=True),
    'type': fields.String(required=True),
    'description': fields.String(required=True),
    'formal_basis': fields.String(required=True),
    'project_justification': fields.String(required=True),
    'additional_info': fields.String(required=True),
    'project_goals': fields.String(required=True),
    'risks': fields.String(required=True),
    'deviations': fields.String(required=True),
}

update_stage_model = {
    'project_id': fields.Integer(required=True),
    'status': fields.String(required=True)
}

set_user_role_model = {
    'user_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True),
    'project_id': fields.Integer(required=True)
}

create_indicator_model = {
    'project_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'evaluation_type': fields.String(required=True),
    'evaluation_frequency': fields.String(required=True),
    'units_measure': fields.String(required=True),
    'base_value': fields.Integer(required=True),
    'base_value_date': fields.String(required=True),
    'description': fields.String(required=True),
    'info_collection': fields.String(required=True),
    'coverage_units': fields.String(required=True),
    'approval_doc': fields.String(required=True)
}

indicator_set_user_role_model = {
    'user_id': fields.Integer(required=True),
    'indicator_role_id': fields.Integer(required=True),
    'indicator_id': fields.Integer(required=True)
}

indicator_remove_user_role_model = {
    **indicator_set_user_role_model
}

update_indicator_model = {
    'indicator_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'evaluation_type': fields.String(required=True),
    'evaluation_frequency': fields.String(required=True),
    'units_measure': fields.String(required=True),
    'base_value': fields.Integer(required=True),
    'base_value_date': fields.String(required=True),
    'description': fields.String(required=True),
    'info_collection': fields.String(required=True),
    'coverage_units': fields.String(required=True),
    'approval_doc': fields.String(required=True)
}

indicator_delete_model = {
    'indicator_id': fields.Integer(required=True)
}

create_indicator_value_model = {
    'indicator_id': fields.Integer(required=True),
    'period': fields.String(required=True),
    'plan_value': fields.String(required=True),
    'forecast_value': fields.String(required=True),
    'actual_value': fields.String(required=True)
}

update_indicator_value_model = {
    'indicator_value_id': fields.Integer(required=True),
    'period': fields.String(required=True),
    'plan_value': fields.String(required=True),
    'forecast_value': fields.String(required=True),
    'actual_value': fields.String(required=True),
}

delete_indicator_value_model = {
    'indicator_value_id': fields.Integer(required=True)
}

upload_file_model = {
    'project_id': fields.Integer(required=True),
    'type': fields.String(required=True)
}

remove_file_model = {
    'file_id': fields.String(required=True),
    'project_id': fields.Integer(required=True),
}
