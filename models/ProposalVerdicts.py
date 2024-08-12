from peewee import AutoField, ForeignKeyField, TextField, DateField
from database import BaseModel
from models import User, Proposal


class ProposalVerdicts(BaseModel):
    id = AutoField(primary_key=True)
    project_proposal = ForeignKeyField(Proposal, on_delete='CASCADE', null=False)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    conclusion = TextField()
    status = TextField()
    date = DateField(null=True)

    def get_dto(self):
        return {
            'id': self.id,
            'project_proposal': {
                'id': self.project_proposal.id,
                'name': self.project_proposal.name,
                'user': {
                    'id': self.project_proposal.user.id,
                    'fullname': f'{self.project_proposal.user.lastname} {self.project_proposal.user.firstname} '
                                f'{self.project_proposal.user.surname}',
                }
            },
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            },
            'conclusion': self.conclusion,
            'status': self.status,
            'date': self.date
        }

    class Meta:
        db_table = 'proposal_verdicts'
