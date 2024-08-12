from peewee import TextField, AutoField, ForeignKeyField, IntegerField, prefetch, FloatField
from database import BaseModel
from models import Project


class ProjectContracts(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    name = TextField(null=False)
    type = TextField(null=False)
    federal_law = TextField(null=False)
    planned_cost = FloatField(null=False)
    cost = FloatField(null=True)
    paid = FloatField(null=True)
    description = TextField(null=True)
    link = TextField(null=True)
    status = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import ProjectContractsUserRole, User, ProjectContractsRole, Project

        contracts = (
            cls
            .select(cls, Project)
            .left_outer_join(Project, on=(Project.id == cls.project))
            .where(condition)
        )

        roles = ProjectContractsUserRole
        user_roles = (
            roles
            .select(roles, User, ProjectContractsRole)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, ProjectContractsRole, on=(ProjectContractsRole.id == roles.role))
        )

        contracts_with_users = prefetch(contracts, user_roles)
        return contracts_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name
            },
            'name': self.name,
            'type': self.type,
            'federal_law': self.federal_law,
            'planned_cost': self.planned_cost,
            'cost': self.cost or 0,
            'paid': self.paid or 0,
            'description': self.description or '',
            'link': self.link or '',
            'status': self.status,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role': user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'project_contracts'
