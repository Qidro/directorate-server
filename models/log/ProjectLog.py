from peewee import TextField, AutoField, ForeignKeyField, DateTimeField, DateField
from database import BaseModel
from models import User, Project


class ProjectLog(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    action = TextField(null=False)
    new_status = TextField(null=True, default=None)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    date_change_out = DateField(null=True, default=None)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import Project, User

        project_log = (
            cls
            .select(cls, Project, User)
            .join_from(cls, Project, on=(cls.project == Project.id))
            .join_from(cls, User, on=(cls.user_change == User.id))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return project_log

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name
            },
            'action': self.action,
            'new_status': self.new_status,
            'author': {
                'id': self.user_change.id,
                'fullname': f'{self.user_change.lastname} {self.user_change.firstname} {self.user_change.surname}',
            },
            'time_change': self.date_change.strftime('%H:%M:%S'),
            'date_change': self.date_change.strftime('%Y-%m-%d'),
            'message': self.message
        }

    class Meta:
        db_table = 'project_log'
