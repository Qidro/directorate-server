from peewee import TextField, AutoField
from database import BaseModel


class ProjectContractsRole(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    slug = TextField(null=False)
    description = TextField(null=True)

    def get_dto(self):
        return{
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description
        }

    class Meta:
        db_table = 'project_contracts_role'
