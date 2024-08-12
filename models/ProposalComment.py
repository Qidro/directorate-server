from peewee import AutoField, ForeignKeyField, TextField, DateField
from database import BaseModel
from models import User, Proposal


class ProposalComment(BaseModel):
    id = AutoField(primary_key=True)
    proposal = ForeignKeyField(Proposal, on_delete='CASCADE', null=False)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    date = DateField(null=False)
    name = TextField()
    realization_period = TextField()
    executors = TextField()
    justification = TextField()
    purpose = TextField()
    results = TextField()
    target_indicators = TextField()
    planned_actions = TextField()
    resources = TextField()
    contacts = TextField()

    def get_dto(self):
        return {
            'id': self.id,
            'proposal': {
                'id': self.proposal.id,
                'user': {
                    'id': self.proposal.user.id,
                    'fullname': f'{self.proposal.user.lastname} {self.proposal.user.firstname} {self.proposal.user.surname}',
                }
            },
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}',
            },
            'date': self.date.strftime('%Y-%m-%d'),
            'name': self.name,
            'realization_period': self.realization_period,
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
        db_table = 'proposal_comments'
