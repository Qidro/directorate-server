from peewee import AutoField, TextField, ForeignKeyField, DateTimeField
from database import BaseModel
from models import User, ProjectCalendarPlan


class ProjectCalendarPlanLog(BaseModel):
    id = AutoField(primary_key=True)
    calendar_plan = ForeignKeyField(ProjectCalendarPlan, on_delete='CASCADE', null=False)
    action = TextField(null=False)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import ProjectCalendarPlan, User

        calendar_plan_log = (
            cls
            .select(cls, ProjectCalendarPlan, User)
            .join_from(cls, ProjectCalendarPlan, on=(cls.calendar_plan == ProjectCalendarPlan.id))
            .join_from(cls, User, on=(cls.user_change == User.id))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return calendar_plan_log

    def get_dto(self):
        return {
            'id': self.id,
            'calendar_plan': {
                'id': self.calendar_plan.id,
                'name': self.calendar_plan.name
            },
            'action': self.action,
            'author': {
                'id': self.user_change.id,
                'fullname': f'{self.user_change.lastname} {self.user_change.firstname} {self.user_change.surname}',
            },
            'time_change': self.date_change.strftime('%H:%M:%S'),
            'date_change': self.date_change.strftime('%Y-%m-%d'),
            'message': self.message
        }

    class Meta:
        db_table = 'project_calendar_plan_log'
