from uuid import uuid4
from peewee import fn, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from exceptions import ApiError
from models import User, Session, UserPosition, Position, UserRight


# Регистрация юзера
def registration(user_login: str, firstname: str, lastname: str, surname: str, password: str, phone: str, email: str,
                 position_id: int):
    if User.select().where(User.login == user_login).exists():
        raise ApiError.BadRequest('Login already exist')

    if not Position.select().where(Position.id == position_id).exists():
        raise ApiError.BadRequest('Position not found')

    user = User(
        login=user_login,
        firstname=firstname,
        lastname=lastname,
        surname=surname,
        password=generate_password_hash(password),
        phone=phone,
        email=email
    )
    user.save()

    user_position = UserPosition(
        user=user,
        position=position_id
    )
    user_position.save()
    user = User.fetch(User.id == user.id)
    return user[0].get_dto()


def edit(user_id: str, user_login: str, firstname: str, lastname: str, surname: str, email: str, position_id: int, user_change):
    user = User.get_or_none(id=user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    if not Position.select().where(Position.id == position_id).exists():
        raise ApiError.BadRequest('Position not found')

    prev_user_data = User.fetch(User.id == user_id)[0].get_dto()

    user.login = user_login
    user.firstname = firstname
    user.lastname = lastname
    user.surname = surname
    user.email = email
    user.save()

    user_position = UserPosition.get_or_none(user=user)
    if user_position:
        user_position.position = position_id
        user_position.save()
    else:
        user_position = UserPosition(
            user=user,
            position=position_id
        )
        user_position.save()

    new_user_data = User.fetch(User.id == user_id)[0].get_dto()

    return new_user_data, prev_user_data


def change_password(user_id: int, password: str):
    user = User.get_or_none(id=user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    user.password = generate_password_hash(password)
    user.save()


# Удаление юзера
def delete(user_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    user.is_Archived = True
    user.save()
    # user = User.delete().where(User.id == user_id)
    # user.execute()


# Авторизация юзера
def login(user_login: str, password: str):
    users = User.fetch(User.login == user_login)
    if len(users) == 0 or not check_password_hash(users[0].password, password):
        raise ApiError.BadRequest('Wrong login or password')

    if users[0].is_Archived:
        raise ApiError.Forbidden()

    user_sessions = Session.select(fn.COUNT(Session.id)).where(Session.user == users[0]).get_or_none()

    if user_sessions.id >= 5:
        delete_session = Session.delete().where(Session.user == users[0]).limit(1)
        delete_session.execute()

    session = Session(user=users[0], session=str(uuid4()))
    session.save()

    return users[0].get_dto(), session.session


# Проверка авторизации юзера
def checkout(session: str):
    session = Session.get_or_none(session=session)
    if not session:
        raise ApiError.UnauthorizedError()

    users = User.fetch(User.id == session.user)
    if users[0].is_Archived:
        raise ApiError.Forbidden()

    return users[0].get_dto()


# Получение информации аккаунта юзера
def get_user(user_id: int):
    users = User.fetch(User.id == user_id)
    if len(users) == 0:
        raise ApiError.BadRequest('User not found')

    return users[0].get_dto()


# Добавлене прав юзеру
def add_right(user_id, right_id):
    try:
        if UserRight.select().where(UserRight.user == user_id, UserRight.right == right_id).exists():
            raise ApiError.BadRequest('This user already has this right')

        user_right = UserRight.create(user=user_id, right=right_id)
        return user_right.get_dto()
    except IntegrityError:
        raise ApiError.BadRequest('User or right not found')


# Удаление прав у юзера
def remove_right(user_id, right_id):
    user_right = UserRight.get_or_none(UserRight.user == user_id, UserRight.right == right_id)
    if not user_right:
        return

    UserRight.delete().where(UserRight.id == user_right).execute()
    return user_right.get_dto()


def get_users():
    users = User.fetch()
    return [user.get_dto() for user in users if not user.is_Archived]


def get_archive_user():
    users = User.fetch(User.is_Archived == True)
    if not users:
        raise ApiError.BadRequest('User not found')
    return [user.get_dto() for user in users]
