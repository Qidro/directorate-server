from webargs import fields

create_budget_model = {
    'project_id': fields.Integer(required=True),
    'stage_id': fields.Integer(required=True),
    'funding_source': fields.String(required=True),
    'costs_name': fields.String(required=True),
    'spending_costs': fields.Float(required=True, allow_none=True)
}

edit_budget_model = {
    'budget_id': fields.Integer(required=True),
    'funding_source': fields.String(required=True),
    'costs_name': fields.String(required=True),
    'spending_costs': fields.Float(required=True, allow_none=True)
}

delete_budget_model = {
    'budget_id': fields.Integer(required=True)
}