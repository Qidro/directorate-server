from peewee import TextField, AutoField, ForeignKeyField, DateTimeField
from database import BaseModel
from models import User, Backpack


class BackpackLog(BaseModel):
    id = AutoField(primary_key=True)
    backpack = ForeignKeyField(Backpack, on_delete='CASCADE', null=False)
    action = TextField(null=False)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import Backpack, User

        backpack_log = (
            cls
            .select(cls, Backpack, User)
            .join_from(cls, Backpack, on=(cls.backpack == Backpack.id))
            .join_from(cls, User, on=(cls.user_change == User.id))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return backpack_log

    def get_dto(self):
        return {
            'id': self.id,
            'backpack': {
                'id': self.backpack.id,
                'name': self.backpack.name
            },
            'action': self.action,
            'author': {
                'id': self.user_change.id,
                'fullname': f'{self.user_change.lastname} {self.user_change.firstname} {self.user_change.surname}',
            },
            'time_change': self.date_change.strftime('%H:%M:%S'),
            'date_change': self.date_change.strftime('%Y-%m-%d'),
            'message': self.message
        }

    class Meta:
        db_table = 'backpack_log'
