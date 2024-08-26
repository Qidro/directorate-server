from flask import Blueprint, request, jsonify, make_response, Response
from webargs import flaskparser
from decorators import login_required, rights_required
from exceptions import ApiError
from .fields import register_model, login_model, delete_user_model, right_model, edit_model, change_password_model
from service import user_service
from service.log import user_service_log

user_router = Blueprint('user', __name__)


@user_router.post('/user/registration')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def register(user):
    data = flaskparser.parser.parse(register_model, request)
    user_data = user_service.registration(data['login'], data['firstname'], data['lastname'], data['surname'], data['password'], data['phone'], data['email'], data['position_id'])
    return jsonify(user_data)

@user_router.post('/user/NewRegistration')
def register_new():
    data = flaskparser.parser.parse(register_model, request)
    user_data = user_service.registration(data['login'], data['firstname'], data['lastname'], data['surname'], data['password'], data['phone'], data['email'], data['position_id'])
    return jsonify(user_data)


@user_router.post('/user/edit')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def edit(user):
    data = flaskparser.parser.parse(edit_model, request)
    user_data, prev_user_data = user_service.edit(data['user_id'], data['login'], data['firstname'], data['lastname'], data['surname'], data['email'], data['position_id'], user)

    user_service_log.user_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        user_dto=user_data,
        prev_user_dto=prev_user_data,
        action='UPDATE_USER'
    )

    return jsonify(user_data)


@user_router.post('/user/change_password')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def change_password(user):
    data = flaskparser.parser.parse(change_password_model, request)
    user_service.change_password(data['user_id'], data['password'])
    return Response(status=200)


@user_router.post('/user/login')
def login():
    data = flaskparser.parser.parse(login_model, request)
    user, session = user_service.login(data['login'], data['password'])

    res = make_response(jsonify(user))
    res.set_cookie('session', session, httponly=True)
    return res


@user_router.get('/user/checkout')
def checkout():
    session = request.cookies.get('session')
    if not session:
        raise ApiError.UnauthorizedError()

    user = user_service.checkout(session)
    return jsonify(user)


@user_router.post('/user/logout')
@login_required
def logout(user):
    res = make_response(Response(status=200))
    res.set_cookie('session', '', httponly=True)
    return res


@user_router.get('/user/<int:user_id>')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_user(user, user_id):
    user = user_service.get_user(user_id)
    return jsonify(user)


@user_router.post('/user/rights/add')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def add_right(user):
    data = flaskparser.parser.parse(right_model, request)
    user_right = user_service.add_right(data['user_id'], data['right_id'])

    user_service_log.user_right_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        user_right_dto=user_right,
        action='SET_RIGHT'
    )

    return jsonify(user_right['right'])


@user_router.delete('/user/rights/remove')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def remove_right(user):
    data = flaskparser.parser.parse(right_model, request)
    user_right = user_service.remove_right(data['user_id'], data['right_id'])

    user_service_log.user_right_log(
        author_id=user.id,
        author_name=user.get_dto()['fullname'],
        user_right_dto=user_right,
        action='REMOVE_RIGHT'
    )

    return Response(status=204)


@user_router.delete('/user/delete')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def delete_user(user):
    data = flaskparser.parser.parse(delete_user_model, request)
    user_service.delete(data['user_id'])
    return Response(status=204)


@user_router.get('/users')
@login_required
def get_users(user):
    user_list = user_service.get_users()
    return jsonify(user_list)


@user_router.get('/user/<int:user_id>/logs&position=<int:position>')
@login_required
@rights_required(['SYSTEM_ADMIN'])
def get_backpack_logs(user, user_id, position):
    logs = user_service_log.get_user_logs(user_id, position)
    return jsonify(logs)

