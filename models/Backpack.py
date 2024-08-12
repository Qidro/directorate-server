import datetime

from peewee import TextField, AutoField, BooleanField, DateField, prefetch
from database import BaseModel


class Backpack(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False, unique=False)
    description = TextField(null=False, unique=False)
    is_Archived = BooleanField(default=False)
    creation_date = DateField(null=False, default=datetime.date.today())
    change_date = DateField(null=True)

    @classmethod
    def fetch(cls, condition=None):
        from models import BackpackUserRole, User, BackpackRole

        backpacks = \
            cls\
            .select()\
            .left_outer_join(BackpackUserRole, on=(BackpackUserRole.backpack == cls.id))\
            .where(condition)\
            .group_by(cls.id)

        roles = BackpackUserRole
        user_roles = (
            roles
            .select(roles, User, BackpackRole)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, BackpackRole, on=(BackpackRole.id == roles.role))
        )

        backpacks_with_users = prefetch(backpacks, user_roles)
        return backpacks_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creation_date': self.creation_date.strftime('%Y-%m-%d'),
            'change_date': self.change_date.strftime('%Y-%m-%d') if self.change_date else None,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role': user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'backpacks'
