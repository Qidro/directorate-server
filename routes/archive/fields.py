from webargs import fields

backpack_model = {
    'backpack_id': fields.Integer(required=True)
}

project_model = {
    'project_id': fields.Integer(required=True)
}

proposal_model = {
    'proposal_id': fields.Integer(required=True)
}

user_model = {
    'user_id': fields.Integer(required=True)
}
