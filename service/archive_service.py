from exceptions import ApiError
from models import Backpack, User, Project, Proposal


def get_backpacks_archive():
    backpacks = Backpack.fetch(Backpack.is_Archived == True)
    return [backpack.get_dto() for backpack in backpacks]


def unzip_backpack(backpack_id: int):
    backpack = Backpack.get_or_none((Backpack.id == backpack_id) & (Backpack.is_Archived == True))
    if not backpack:
        raise ApiError.BadRequest('Backpack not found')

    backpack.is_Archived = False
    backpack.save()
    return backpack.get_dto()


def get_projects_archive():
    projects = Project.fetch(Project.is_Archived == True)
    return [project.get_dto() for project in projects]


def unzip_project(project_id: int):
    project = Project.get_or_none((Project.id == project_id) & (Project.is_Archived == True))
    if not project:
        raise ApiError.BadRequest('Project not found')

    project.is_Archived = False
    project.status = "INITIATION"
    project.save()
    return project.get_dto()


def get_proposals_archive():
    proposals = Proposal.fetch(Proposal.isArchived == True)
    return [proposal.get_dto() for proposal in proposals]


def unzip_proposal(proposal_id: int):
    proposal = Proposal.get_or_none((Proposal.id == proposal_id) & (Proposal.isArchived == True))
    if not proposal:
        raise ApiError.BadRequest('Proposal not found')

    proposal.isArchived = False
    proposal.status = "REVIEW"
    proposal.save()
    return proposal.get_dto()


def get_user_archive():
    users = User.fetch(User.is_Archived == True)
    return [user.get_dto() for user in users]


def unzip_user(user_id: int):
    user = User.fetch((User.id == user_id) & (User.is_Archived == True))
    if len(user) == 0:
        raise ApiError.BadRequest('User not found')

    user[0].is_Archived = False
    user[0].save()
    return user[0].get_dto()
