from models import Right


def get_rights():
    rights = [right.get_dto() for right in Right.select()]
    return rights

