from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, ProjectRole, Project


class ProjectUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, backref='project_role', on_delete='CASCADE', null=False)
    role = ForeignKeyField(ProjectRole, on_delete='CASCADE', null=False)
    project = ForeignKeyField(Project, backref='users_role', on_delete='CASCADE', null=False)


    class Meta:
        db_table = 'project_user_role'
