from peewee import AutoField, ForeignKeyField, IntegerField, TextField, FloatField
from database import BaseModel
from models import ProjectCalendarPlan, Project


class ProjectBudget(BaseModel):
    id = AutoField(primary_key=True)
    project = ForeignKeyField(Project, on_delete='CASCADE', null=False)
    stage = ForeignKeyField(ProjectCalendarPlan, on_delete='CASCADE', null=False)
    funding_source = TextField(null=False)
    costs_name = TextField(null=False)
    spending_costs = FloatField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'project_id': self.project.id,
            'stage': {
                'id': self.stage.id,
                'name': self.stage.name,
                'type': self.stage.type
            },
            'funding_source': self.funding_source,
            'costs_name': self.costs_name,
            'spending_costs': self.spending_costs
        }

    @classmethod
    def fetch(cls, condition=None):
        from models import Project, ProjectCalendarPlan

        budget = (
            cls
            .select(cls, Project, ProjectCalendarPlan)
            .join_from(cls, Project, on=(cls.project == Project.id))
            .join_from(cls, ProjectCalendarPlan, on=(cls.stage == ProjectCalendarPlan.id))
            .where(condition)
        )
        return budget

    class Meta:
        db_table = 'project_budget'
