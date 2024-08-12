from peewee import AutoField, ForeignKeyField
from database import BaseModel
from models import ProjectResults, ProjectCalendarPlan


class ProjectCalendarPlanResults(BaseModel):
    id = AutoField(primary_key=True)
    calendar_plan = ForeignKeyField(ProjectCalendarPlan, backref='project_results', on_delete='CASCADE', null=False)
    result = ForeignKeyField(ProjectResults, on_delete='CASCADE', null=False)

    @classmethod
    def fetch(cls, condition=None):
        return (
            cls
            .select(cls, ProjectResults)
            .left_outer_join(ProjectResults, on=(cls.result == ProjectResults.id))
            .where(condition)
        )

    def get_dto(self):
        return {
            'id': self.id,
            'calendar_plan_id': self.calendar_plan.id,
            'result': {
                'id': self.result.id,
                'name': self.result.name,
                'status': self.result.status
            }
        }

    class Meta:
        db_table = 'project_calendar_plan_results'
