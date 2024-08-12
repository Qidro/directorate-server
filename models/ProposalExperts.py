from peewee import AutoField, ForeignKeyField, TextField, DateField
from database import BaseModel
from models import User, Proposal


class ProposalExperts(BaseModel):
    id = AutoField(primary_key=True)
    project_proposal = ForeignKeyField(Proposal, backref="experts", on_delete='CASCADE', null=False)
    user = ForeignKeyField(User, on_delete='CASCADE', null=False)
    verification_status = TextField(null=False)
    date_verification = DateField(null=True, default=None)
    date_appointment = DateField(null=False)
    director = ForeignKeyField(User, on_delete='CASCADE', null=False)

    def get_dto(self):
        return {
            'id': self.id,
            'project_proposal': {
                'id': self.project_proposal.id,
                'name': self.project_proposal.name
            },
            'user': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            },
            'verification_status': self.verification_status,
            'date_verification': self.date_verification,
            'date_appointment': self.date_appointment,
            'director': {
                'id': self.user.id,
                'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}'
            }
        }

    def get_small_dto(self):
        return {
            'id': self.id,
            'user_id': self.user.id,
            'fullname': f'{self.user.lastname} {self.user.firstname} {self.user.surname}',
            'verification_status': self.verification_status
        }

    class Meta:
        db_table = 'proposal_experts'
