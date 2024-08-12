from webargs import fields

create_model = {
    'name': fields.String(required=True),
    'description': fields.String(required=True)
}

user_role_model = {
    'user_id': fields.Integer(required=True),
    'role_id': fields.Integer(required=True),
    'backpack_id': fields.Integer(required=True)
}

delete_model = {
    'backpack_id': fields.Integer(required=True)
}

update_model = {
    'backpack_id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True)
}

upload_file_model = {
    'backpack_id': fields.Integer(required=True),
    'type': fields.String(required=True)
}

remove_file_model = {
    'file_id': fields.String(required=True),
    'backpack_id': fields.Integer(required=True),
}
