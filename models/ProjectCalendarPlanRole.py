from peewee import TextField, AutoField
from database import BaseModel


class ProjectCalendarPlanRole(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    slug = TextField(null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }

    class Meta:
        db_table = 'project_calendar_plan_role'
        