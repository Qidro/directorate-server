import datetime

from peewee import AutoField, ForeignKeyField, TextField, BooleanField, DateField, prefetch
from database import BaseModel
from models import User


class Proposal(BaseModel):
    id = AutoField(primary_key=True)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    status = TextField(null=False)
    submission_date = DateField(null=False)
    name = TextField(null=False)
    realization_period_start = DateField(null=False)
    realization_period_end = DateField(null=False)
    executors = TextField(null=False)
    justification = TextField(null=False)
    purpose = TextField(null=False)
    results = TextField(null=False)
    target_indicators = TextField(null=False)
    planned_actions = TextField(null=False)
    resources = TextField(null=False)
    contacts = TextField(null=False)
    isArchived = BooleanField(default=False)

    @classmethod
    def fetch(cls, condition=None):
        from models import ProposalExperts, User

        proposals = (
            cls
            .select(cls, User)
            .join(User, on=(User.id == cls.user))
            .where(condition)
            .group_by(cls.id)
        )

        experts = (
            ProposalExperts
            .select(ProposalExperts, User)
            .join(User, on=(User.id == ProposalExperts.user))
        )

        proposals_with_experts = prefetch(proposals, experts)
        return proposals_with_experts

    def get_dto(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            },
            'status': self.status,
            'submission_date': self.submission_date,
            'name': self.name,
            'realization_period': [self.realization_period_start, self.realization_period_end],
            'executors': self.executors,
            'justification': self.justification,
            'purpose': self.purpose,
            'results': self.results,
            'target_indicators': self.target_indicators,
            'planned_actions': self.planned_actions,
            'resources': self.resources,
            'contacts': self.contacts,
            'isArchived': self.isArchived,
            'experts': [expert.get_small_dto() for expert in self.experts]
        }

    def get_dto_log(self):
        return {
            'id': self.id,
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            },
            'status': self.status,
            'submission_date': self.submission_date,
            'name': self.name,
            'realization_period_start': self.realization_period_start.strftime('%Y-%m-%d'),
            'realization_period_end': self.realization_period_end.strftime('%Y-%m-%d'),
            'executors': self.executors,
            'justification': self.justification,
            'purpose': self.purpose,
            'results': self.results,
            'target_indicators': self.target_indicators,
            'planned_actions': self.planned_actions,
            'resources': self.resources,
            'contacts': self.contacts
        }

    class Meta:
        db_table = 'proposal'
