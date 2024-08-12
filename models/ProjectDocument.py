from peewee import AutoField, ForeignKeyField, TextField
from database import BaseModel
from models import Project, File


class ProjectDocument(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    file = ForeignKeyField(File, on_delete='CASCADE', null=False)
    type = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None):
        return (
            cls
            .select(cls, File)
            .left_outer_join(File, on=(cls.file == File.id))
            .where(condition)
        )

    def get_dto(self):
        return {
            **self.file.get_dto(),
            'type': self.type
        }

    class Meta:
        db_table = 'project_documents'
