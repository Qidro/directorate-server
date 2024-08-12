from peewee import TextField, AutoField, ForeignKeyField
from database import BaseModel
from models import Department


class Position(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    department = ForeignKeyField(Department, backref='positions', on_delete='CASCADE', null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name
        }

    class Meta:
        db_table = 'positions'
