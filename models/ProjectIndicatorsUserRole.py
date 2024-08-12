from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, ProjectIndicatorsRole, ProjectIndicators


class ProjectIndicatorsUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='indicators_role', on_delete='CASCADE', null=False)
    role = ForeignKeyField(ProjectIndicatorsRole, on_delete='CASCADE', null=False)
    indicator = ForeignKeyField(ProjectIndicators, backref='users_role', on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'project_indicators_user_role'
