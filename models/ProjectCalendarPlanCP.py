from peewee import AutoField, TextField
from database import BaseModel


class ProjectCalendarPlanCP(BaseModel):
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
        db_table = 'project_calendar_plan_cp'
