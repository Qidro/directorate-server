from peewee import TextField, AutoField, ForeignKeyField, prefetch
from database import BaseModel
from models import Project


class ProjectResults(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    name = TextField(null=False)
    type = TextField(null=False)
    units_measure = TextField(null=False)
    characteristic = TextField(null=False)
    approval_doc = TextField(null=True)
    status = TextField(null=True)

    @classmethod
    def fetch(cls, condition=None):
        from models import ProjectResultsUserRole, User, ProjectResultsRoles

        project_results = cls.select().where(condition)

        roles = ProjectResultsUserRole
        user_roles = (
            roles
            .select(roles, User, ProjectResultsRoles)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, ProjectResultsRoles, on=(ProjectResultsRoles.id == roles.role))
        )

        project_results_with_users = prefetch(project_results, user_roles)
        return project_results_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name
            },
            'name': self.name,
            'type': self.type,
            'units_measure': self.units_measure,
            'characteristic': self.characteristic,
            'approval_doc': self.approval_doc,
            'status': self.status,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role':  user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'project_results'
