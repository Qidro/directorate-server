from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, ProjectResultsRoles, ProjectResults


class ProjectResultsUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    role = ForeignKeyField(ProjectResultsRoles, on_delete='CASCADE', null=False)
    project_result = ForeignKeyField(ProjectResults, backref='users_role', on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'project_results_user_role'