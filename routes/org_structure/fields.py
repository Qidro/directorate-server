from webargs import fields


create_department_model = {
    'name': fields.String(required=True)
}

edit_department_model = {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True)
}

delete_department_model = {
    'id': fields.Integer(required=True)
}

create_position_model = {
    'name': fields.String(required=True),
    'department_id': fields.Integer(required=True)
}

edit_position_model = {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True)
}

delete_position_model = {
    'id': fields.Integer(required=True)
}
