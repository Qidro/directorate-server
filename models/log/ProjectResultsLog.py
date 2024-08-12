from peewee import AutoField, ForeignKeyField, TextField, DateTimeField
from database import BaseModel
from models import User, ProjectResults


class ProjectResultsLog(BaseModel):
    id = AutoField(primary_key=True)
    result = ForeignKeyField(ProjectResults, on_delete='CASCADE', null=False)
    action = TextField(null=False)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import User, ProjectResults

        user_log = (
            cls
            .select(cls, User, ProjectResults)
            .join(ProjectResults, on=(cls.result == ProjectResults.id))
            .join(User, on=(cls.user_change == User.id))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return user_log

    def get_dto(self):
        return {
            'id': self.id,
            'result': {
                'id': self.result.id,
                'name': self.result.name,
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
        db_table = 'project_result_log'
