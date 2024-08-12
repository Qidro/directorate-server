from peewee import TextField, AutoField, ForeignKeyField, DateField
from database import BaseModel
from models import ProjectIndicators


class ProjectIndicatorsValues(BaseModel):
    id = AutoField(primary_key=True)
    indicator = ForeignKeyField(ProjectIndicators, on_delete='CASCADE', null=False)
    period = DateField(null=False)
    plan = TextField(null=True)
    forecast = TextField(null=True)
    actual = TextField(null=True)
    status = TextField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'indicator': {
                'id': self.indicator.id,
                'name': self.indicator.name
            },
            'period': self.period,
            'plan_value': self.plan,
            'forecast_value': self.forecast,
            'actual_value': self.actual,
            'status': self.status
        }

    class Meta:
        db_table = 'project_indicators_values'
