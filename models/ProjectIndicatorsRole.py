from peewee import TextField, AutoField
from database import BaseModel


class ProjectIndicatorsRole(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False, unique=False)
    slug = TextField(null=False, unique=False)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }

    class Meta:
        db_table = 'project_indicators_role'
