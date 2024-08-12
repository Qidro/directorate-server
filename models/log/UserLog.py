from peewee import AutoField, ForeignKeyField, TextField, DateTimeField
from database import BaseModel
from models import User


class UserLog(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    action = TextField(null=False)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import User

        OpponentUser = User.alias()
        user_log = (
            cls
            .select(cls, User, OpponentUser)
            .join(User, on=(cls.user == User.id))
            .join(OpponentUser, on=(cls.user_change == OpponentUser.id).alias('user_change'))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return user_log

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}',
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
        db_table = 'user_log'
