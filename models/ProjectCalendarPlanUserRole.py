from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import User, ProjectCalendarPlanRole, ProjectCalendarPlan


class ProjectCalendarPlanUserRole(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    role = ForeignKeyField(ProjectCalendarPlanRole, on_delete='CASCADE', null=False)
    calendar_plan = ForeignKeyField(ProjectCalendarPlan, backref='users_role', on_delete='CASCADE', null=False)

    class Meta:
        db_table = 'project_calendar_plan_user_role'
