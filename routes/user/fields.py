from webargs import fields

register_model = {
    'login': fields.String(required=True),
    'firstname': fields.String(required=True),
    'lastname': fields.String(required=True),
    'surname': fields.String(missing=None),
    'password': fields.String(required=True),
    'phone': fields.String(required=False, load_default=None),
    'email': fields.String(required=True),
    'position_id': fields.Integer(required=True)
}

edit_model = {
    "user_id": fields.Integer(required=True),
    "login": fields.String(required=True),
    "firstname": fields.String(required=True),
    "lastname": fields.String(required=True),
    "surname": fields.String(required=True),
    "email": fields.String(required=True),
    "position_id": fields.Integer(required=True)
}

change_password_model = {
    'user_id': fields.Integer(required=True),
    'password': fields.String(required=True)
}

login_model = {
    'login': fields.String(required=True),
    'password': fields.String(required=True)
}

right_model = {
    'user_id': fields.Integer(required=True),
    'right_id': fields.Integer(required=True)
}

delete_user_model = {
    'user_id': fields.Integer(required=True)
}
