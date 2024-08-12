from flask import request
from exceptions import ApiError
from models import Session, User


def login_required(fn):
    def wrapper(*args, **kwargs):
        user_session = request.cookies.get('session')
        if not user_session:
            raise ApiError.UnauthorizedError()

        session = Session.select().where(Session.session == user_session).get_or_none()
        if session is None:
            raise ApiError.UnauthorizedError()

        user = User.fetch(User.id == session.user)[0]

        return fn(user, *args, **kwargs)

    wrapper.__name__ = fn.__name__
    return wrapper
