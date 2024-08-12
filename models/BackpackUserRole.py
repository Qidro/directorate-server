from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import Backpack, User, BackpackRole


class BackpackUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    role = ForeignKeyField(BackpackRole, on_delete='CASCADE', null=False)
    backpack = ForeignKeyField(Backpack, backref='users_role', on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'backpack_user_role'
