from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, Right


class UserRight(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='rights', on_delete='CASCADE', null=False)
    right = ForeignKeyField(Right, on_delete='CASCADE', null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            },
            'right': self.right.get_dto()
        }

    class Meta:
        db_table = 'users_rights'
