from webargs import fields

create_contract_model = {
    'project_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'federal_law': fields.String(required=True),
    'planned_cost': fields.Float(required=True),
    'cost': fields.Float(required=False, load_default=None),
    'paid': fields.Float(required=False, load_default=None),
    'description': fields.String(required=False, load_default=None),
    'link': fields.String(required=False, load_default=None)
}

edit_contract_model = {
    'contract_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'type': fields.String(required=True),
    'federal_law': fields.String(required=True),
    'planned_cost': fields.Float(required=True),
    'cost': fields.Float(required=False, load_default=None),
    'paid': fields.Float(required=False, load_default=None),
    'description': fields.String(required=False, load_default=None),
    'link': fields.String(required=False, load_default=None)
}

remove_contract_model = {
    'contract_id': fields.Integer(required=True)
}

set_user_role_model = {
    'contract_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True)
}

set_stage_model = {
    'contract_id': fields.Integer(required=True),
    'status': fields.String(required=True)
}

upload_file_model = {
    'contract_id': fields.Integer(required=True),
    'type': fields.String(required=True)
}

remove_file_model = {
    'file_id': fields.String(required=True),
    'contract_id': fields.Integer(required=True),
}
