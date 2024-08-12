from webargs import fields

set_expert_model = {
    'proposal_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True)
}

remove_expert_model = {
    'proposal_id': fields.Integer(required=True),
    'user_id': fields.Integer(required=True)
}

set_verdict_model = {
    'proposal_id': fields.Integer(required=True),
    'conclusion': fields.String(required=True),
    'status': fields.String(required=True)
}

create_model = {
    'name': fields.String(required=True),
    'realization_period_start': fields.Date(required=True),
    'realization_period_end': fields.Date(required=True),
    'executors': fields.String(required=True),
    'justification': fields.String(required=True),
    'purpose': fields.String(required=True),
    'results': fields.String(required=True),
    'target_indicators': fields.String(required=True),
    'planned_actions': fields.String(required=True),
    'resources': fields.String(required=True),
    'contacts': fields.String(required=True)
}


update_model = {
    **create_model,
    'id': fields.Integer(required=True),
}

add_comment_model = {
    'proposal': fields.Integer(required=True),
    'status': fields.String(required=True),
    'name': fields.String(required=True),
    'realization_period': fields.String(required=True),
    'executors': fields.String(required=True),
    'justification': fields.String(required=True),
    'purpose': fields.String(required=True),
    'results': fields.String(required=True),
    'target_indicators': fields.String(required=True),
    'planned_actions': fields.String(required=True),
    'resources': fields.String(required=True),
    'contacts': fields.String(required=True)
}