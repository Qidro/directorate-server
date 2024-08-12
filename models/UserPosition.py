from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, Position


class UserPosition(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='positions', on_delete='CASCADE', null=False)
    position = ForeignKeyField(Position, on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'users_position'
