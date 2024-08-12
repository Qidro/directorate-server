from exceptions import ApiError
from models import Department, Position


# Получение списка всех отделов
def get_departments():
    departments = [department.get_dto() for department in Department.fetch()]
    return departments


def get_department(department_id: int):
    department = Department.fetch(Department.id == department_id)
    if len(department) == 0:
        raise ApiError.BadRequest('Department not found')

    return department[0].get_dto()


# Создание отдела
def create_department(name: str):
    department = Department.get_or_none(name=name)
    if department:
        raise ApiError.BadRequest('Department already exist')

    department = Department(name=name)
    department.save()

    department = Department.fetch(Department.id == department.id)[0]
    return department.get_dto()


def edit_department(department_id: int, name: str):
    department = Department.get_or_none(id=department_id)
    if not department:
        raise ApiError.BadRequest('Department not found')

    department = Department.update(name=name).where(Department.id == department_id)
    department.execute()

    department = Department.fetch(Department.id == department_id)[0]
    return department.get_dto()


# Удаление отдела
def delete_department(department_id: int):
    department = Department.delete().where(Department.id == department_id)
    department.execute()


# Получение списка всех должностей в отделе
def get_positions():
    positions = [position.get_dto() for position in Position.select()]
    return positions


def get_position(position_id: int):
    position = Position.get_or_none(id=position_id)
    if not position:
        raise ApiError.BadRequest('Position not found')

    return position.get_dto()


# Создание должности
def create_position(name: str, department_id: int):
    department = Department.get_or_none(id=department_id)
    if not department:
        raise ApiError.BadRequest('Department not found')

    position = Position.get_or_none(name=name, department=department_id)
    if position:
        raise ApiError.BadRequest('Position already exist')

    position = Position(name=name, department_id=department_id)
    position.save()

    return position.get_dto()


def edit_position(position_id: int, name: str):
    position = Position.get_or_none(id=position_id)
    if not position:
        raise ApiError.BadRequest('Position not found')

    position = Position.update(name=name).where(Position.id == position_id)
    position.execute()

    position = Position.get_or_none(id=position_id)

    return position.get_dto()


# Удаление должности
def delete_position(position_id: int):
    position = Position.delete().where(Position.id == position_id)
    position.execute()
