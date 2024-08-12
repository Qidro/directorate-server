from peewee import AutoField, ForeignKeyField, DateField, IntegerField
from database import BaseModel
from models import ProjectResults


class ProjectResultValues(BaseModel):
    id = AutoField(primary_key=True)
    result = ForeignKeyField(ProjectResults, on_delete='CASCADE', null=False)
    achievement_date = DateField(null=False)
    plan = IntegerField(null=False)
    forecast = IntegerField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'result': {
                'id': self.result.id,
                'name': self.result.name
            },
            'achievement_date': self.achievement_date.strftime('%Y-%m-%d'),
            'units_measure': self.result.units_measure,
            'plan': self.plan,
            'forecast': self.forecast
        }

    class Meta:
        db_table = 'project_result_values'
