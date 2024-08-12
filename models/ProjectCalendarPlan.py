import datetime

from peewee import AutoField, TextField, DateField, ForeignKeyField, IntegerField, prefetch
from database import BaseModel
from models import User, Project


class ProjectCalendarPlan(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    type = TextField(null=False)
    name = TextField(null=False)
    awaiting_result = TextField(null=False)
    start_date_plan = DateField(null=True)
    start_date_forecast = DateField(null=True)
    start_date_fact = DateField(null=True)
    length_of_days = TextField(null=True)
    working_days = IntegerField(null=True)
    end_date_plan = DateField(null=True)
    end_date_forecast = DateField(null=True)
    end_date_fact = DateField(null=True)
    approval_doc = TextField(null=True)
    status = TextField(null=True)
    parent_stage_id = IntegerField(null=True)

    @classmethod
    def fetch(cls, condition=None, order_by=None):
        from models import ProjectCalendarPlanUserRole, User, ProjectCalendarPlanRole, Project

        project_calendar_plan = (
            cls
            .select(cls, Project)
            .left_outer_join(Project, on=(Project.id == cls.project))
            .left_outer_join(ProjectCalendarPlanUserRole, on=(ProjectCalendarPlanUserRole.calendar_plan == cls.id))
            .where(condition)
            .group_by(cls.id)
            .order_by(order_by)
        )

        roles = ProjectCalendarPlanUserRole
        user_roles = (
            roles
            .select(roles, User, ProjectCalendarPlanRole)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, ProjectCalendarPlanRole, on=(ProjectCalendarPlanRole.id == roles.role))
        )

        project_calendar_plan_with_users = prefetch(project_calendar_plan, user_roles)
        return project_calendar_plan_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name
            },
            'type': self.type,
            'name': self.name,
            'awaiting_result': self.awaiting_result,
            'start_date_plan': self.start_date_plan.strftime('%Y-%m-%d') if self.start_date_plan else None,
            'start_date_forecast': self.start_date_forecast.strftime('%Y-%m-%d') if self.start_date_forecast else None,
            'start_date_fact': self.start_date_fact.strftime('%Y-%m-%d') if self.start_date_fact else None,
            'length_of_days': self.length_of_days,
            'working_days': self.working_days,
            'end_date_plan': self.end_date_plan.strftime('%Y-%m-%d') if self.end_date_plan else None,
            'end_date_forecast': self.end_date_forecast.strftime('%Y-%m-%d') if self.end_date_forecast else None,
            'end_date_fact': self.end_date_fact.strftime('%Y-%m-%d') if self.end_date_fact else None,
            'approval_doc': self.approval_doc,
            'status': self.status,
            'parent_stage_id': self.parent_stage_id,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role': user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'project_calendar_plan'
