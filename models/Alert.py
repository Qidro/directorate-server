from peewee import AutoField, TextField
from database import BaseModel


class Alert(BaseModel):
    id = AutoField(primary_key=True)
    text = TextField(null=True)

    def get_dto(self):
        return {
            'text': self.text
        }

    class Meta:
        db_table = 'alert'
