from peewee import TextField, AutoField, prefetch
from database import BaseModel


class Department(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import Position

        departments = cls.select().where(condition)
        positions = Position.select()

        departments_with_positions = prefetch(departments, positions)
        return departments_with_positions

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'positions': [position.get_dto() for position in self.positions]
        }

    class Meta:
        db_table = 'departments'
