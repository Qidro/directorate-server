from peewee import TextField, AutoField, prefetch, BooleanField
from database import BaseModel


class User(BaseModel):
    id = AutoField(primary_key=True)
    login = TextField(null=False, unique=True)
    firstname = TextField(null=False)
    lastname = TextField(null=False)
    surname = TextField(null=True)
    password = TextField(null=False)
    phone = TextField(null=True)
    email = TextField(null=False)
    avatar = TextField(null=True)
    is_Archived = BooleanField(default=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import UserPosition, Position, Department, UserRight

        users = (
            cls
            .select(
                cls,
                Position.id.alias('position_id'),
                Position.name.alias('position_name'),
                Department.id.alias('departament_id'),
                Department.name.alias('departament_name')
            )
            .left_outer_join(UserPosition, on=(UserPosition.user == cls.id))
            .left_outer_join(Position, on=(Position.id == UserPosition.position))
            .left_outer_join(Department, on=(Department.id == Position.department))
            .where(condition)
            .objects()
        )

        rights = UserRight.select()
        users_with_rights = prefetch(users, rights)

        return users_with_rights

    def get_dto(self):
        return {
            'id': self.id,
            'login': self.login,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'surname': self.surname,
            'fullname': f'{self.lastname} {self.firstname} {self.surname}',
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'rights': [user_right.right.get_dto() for user_right in self.rights],
            'position': {
                'id': self.position_id,
                'name': self.position_name,
                'department': {
                    'id': self.departament_id,
                    'name': self.departament_name,
                }
            },
            'is_Archived': self.is_Archived
        }

    class Meta:
        db_table = 'users'
