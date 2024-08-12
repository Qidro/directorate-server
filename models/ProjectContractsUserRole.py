from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, ProjectContractsRole, ProjectContracts


class ProjectContractsUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    role = ForeignKeyField(ProjectContractsRole, on_delete='CASCADE', null=False)
    contract = ForeignKeyField(ProjectContracts, backref='users_role', on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'project_contracts_user_role'
