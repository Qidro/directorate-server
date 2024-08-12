from peewee import TextField, AutoField
from database import BaseModel


class Right(BaseModel):
    id = AutoField(primary_key=True)
    slug = TextField(null=False)
    name = TextField(null=False)
    description = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'description': self.description
        }

    class Meta:
        db_table = 'rights'
