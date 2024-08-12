import datetime

from peewee import TextField, AutoField, BooleanField, ForeignKeyField, CharField, DateField, prefetch, IntegerField
from database import BaseModel
from models import Backpack


class Project(BaseModel):
    id = AutoField(primary_key=True)
    backpack = ForeignKeyField(Backpack, on_delete='CASCADE', null=False)
    name = TextField(null=False)
    short_name = CharField(null=True)
    priority = TextField(null=False)
    type = TextField(null=False)
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    description = TextField(null=True)
    formal_basis = TextField(null=True)
    project_justification = TextField(null=True)
    additional_info = TextField(null=True)
    project_goals = TextField(null=True)
    risks = TextField(null=True)
    deviations = TextField(null=True)
    creation_date = DateField(null=False, default=datetime.date.today())
    last_change_date = DateField(null=True)
    status = TextField(null=False)
    is_Archived = BooleanField(default=False)
    proposal_id = IntegerField(null=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import ProjectUserRole, User, ProjectRole

        projects = (
            cls
            .select()
            .left_outer_join(ProjectUserRole, on=(ProjectUserRole.project == cls.id))
            .where(condition)
            .group_by(cls.id)
        )

        roles = ProjectUserRole
        user_roles = (
            roles
            .select(roles, User, ProjectRole)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, ProjectRole, on=(ProjectRole.id == roles.role))
        )

        projects_with_users = prefetch(projects, user_roles)
        return projects_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'backpack': {
                'id': self.backpack.id,
                'name': self.backpack.name,
                'description': self.backpack.description
            },
            'name': self.name,
            'short_name': self.short_name,
            'priority': self.priority,
            'type': self.type,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'description': self.description,
            'formal_basis': self.formal_basis,
            'project_justification': self.project_justification,
            'additional_info': self.additional_info,
            'project_goals': self.project_goals,
            'risks': self.risks,
            'deviations': self.deviations,
            'creation_date': self.creation_date.strftime('%Y-%m-%d') if self.creation_date else None,
            'last_change_date': self.last_change_date.strftime('%Y-%m-%d') if self.last_change_date else None,
            'status': self.status,
            'isArchived': self.is_Archived,
            'proposal_id': self.proposal_id,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role': user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'projects'
