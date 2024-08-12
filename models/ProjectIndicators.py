from peewee import TextField, AutoField, ForeignKeyField, DateField, IntegerField, prefetch
from database import BaseModel
from models import Project


class ProjectIndicators(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    name = TextField(null=False)
    evaluation_type = TextField(null=False)
    evaluation_frequency = TextField(null=False)
    units_measure = TextField(null=True)
    base_value = IntegerField(null=False)
    base_value_date = DateField(null=True)
    description = TextField(null=False)
    info_collection = TextField(null=True)
    coverage_units = TextField(null=True)
    approval_doc = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import ProjectIndicatorsUserRole, User, ProjectIndicatorsRole

        indicators = cls.select().where(condition)

        roles = ProjectIndicatorsUserRole
        user_roles = (
            roles
            .select(roles, User, ProjectIndicatorsRole)
            .join_from(roles, User, on=(User.id == roles.user))
            .join_from(roles, ProjectIndicatorsRole, on=(ProjectIndicatorsRole.id == roles.role))
        )

        indicators_with_users = prefetch(indicators, user_roles)
        return indicators_with_users

    def get_dto(self):
        return {
            'id': self.id,
            'project': {
                'id': self.project.id,
                'name': self.project.name
            },
            'name': self.name,
            'evaluation_type': self.evaluation_type,
            'evaluation_frequency': self.evaluation_frequency,
            'units_measure': self.units_measure,
            'base_value': self.base_value,
            'base_value_date': self.base_value_date,
            'description': self.description,
            'info_collection': self.info_collection,
            'coverage_units': self.coverage_units,
            'approval_doc': self.approval_doc,
            'users': [{
                'id': user_role.user.id,
                'fullname': f'{user_role.user.lastname} {user_role.user.firstname} {user_role.user.surname}',
                'role': user_role.role.get_dto()
            } for user_role in self.users_role]
        }

    class Meta:
        db_table = 'project_indicators'
