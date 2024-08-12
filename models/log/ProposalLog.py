from peewee import AutoField, ForeignKeyField, TextField, DateTimeField
from database import BaseModel
from models import User, Proposal


class ProposalLog(BaseModel):
    id = AutoField(primary_key=True)
    proposal = ForeignKeyField(Proposal, on_delete='CASCADE', null=False)
    user_change = ForeignKeyField(User, null=False)
    date_change = DateTimeField(null=False)
    action = TextField(null=False)
    message = TextField(null=False)

    @classmethod
    def fetch(cls, condition=None, order_by=None, offset=None, limit=None):
        from models import Proposal, User

        proposal_log = (
            cls
            .select(cls, Proposal, User)
            .join_from(cls, Proposal, on=(cls.proposal == Proposal.id))
            .join_from(cls, User, on=(cls.user_change == User.id))
            .where(condition)
            .order_by(order_by)
            .offset(offset)
            .limit(limit)
        )

        return proposal_log

    def get_dto(self):
        return {
            'id': self.id,
            'proposal': {
                'id': self.proposal.id,
                'name': self.proposal.name
            },
            'action': self.action,
            'author': {
                'id': self.user_change.id,
                'fullname': f'{self.user_change.lastname} {self.user_change.firstname} {self.user_change.surname}',
            },
            'time_change': self.date_change.strftime('%H:%M:%S'),
            'date_change': self.date_change.strftime('%Y-%m-%d'),
            'message': self.message
        }

    class Meta:
        db_table = 'proposal_log'
