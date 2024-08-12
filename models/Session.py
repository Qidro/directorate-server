from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import User


class Session(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='sessions', on_delete='CASCADE', null=False)
    session = TextField(null=False)

    class Meta:
        db_table = 'sessions'
