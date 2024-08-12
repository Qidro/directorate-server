from werkzeug.datastructures import FileStorage
from exceptions import ApiError
from models import ProjectContracts, User, ProjectContractsRole, \
    ProjectContractsUserRole, ProjectContractsDocument
from constants.constants import contracts_status_list
from service import file_service

UPLOAD_FOLDER = 'documents'
ALLOWED_EXTENSIONS = (['txt', 'pdf', 'doc', 'docx', 'xlsx'])


def create_contract(
        project_id: int, name: str, type: str,
        federal_law: str, planned_cost: float, cost: float, paid: float,
        description: str, link: str
):
    project_contract = ProjectContracts(
        project=project_id,
        name=name,
        type=type,
        federal_law=federal_law,
        planned_cost=planned_cost,
        cost=cost,
        paid=paid,
        description=description,
        link=link,
        status='INITIATION'
    )
    project_contract.save()

    return ProjectContracts.fetch(ProjectContracts.id == project_contract)[0].get_dto()


def edit_contract(
        contract_id: int, name: str, type: str,
        federal_law: str, planned_cost: float, cost: float, paid: float,
        description: str, link: str
):
    contract = ProjectContracts.get_or_none(ProjectContracts.id == contract_id)
    if not contract:
        raise ApiError.BadRequest('Contract not found')

    prev_contract_data = ProjectContracts.fetch(ProjectContracts.id == contract_id)[0].get_dto()

    contract.name = name
    contract.type = type
    contract.federal_law = federal_law
    contract.planned_cost = planned_cost
    contract.cost = cost
    contract.paid = paid
    contract.description = description
    contract.link = link
    contract.save()

    new_contract_data = ProjectContracts.fetch(ProjectContracts.id == contract_id)[0].get_dto()

    contract_documents = ProjectContractsDocument.fetch(ProjectContractsDocument.contract == contract_id)
    documents = [doc.get_dto() for doc in contract_documents]

    return {**new_contract_data, 'documents': documents}, {**prev_contract_data, 'documents': documents}


def remove_contract(contract_id: int):
    try:
        contract = ProjectContracts.fetch(ProjectContracts.id == contract_id)[0]
    except IndexError:
        return

    ProjectContracts.delete().where(ProjectContracts.id == contract_id).execute()
    return contract.get_dto()


def get_contracts(project_id: int):
    project_contracts = ProjectContracts.fetch(ProjectContracts.project == project_id)
    return [contract.get_dto() for contract in project_contracts]


def get_contract(contract_id: int):
    project_contract = ProjectContracts.fetch(ProjectContracts.id == contract_id)
    if len(project_contract) == 0:
        raise ApiError.BadRequest('Contract not found')

    contract_documents = ProjectContractsDocument.fetch(ProjectContractsDocument.contract == contract_id)
    documents = [doc.get_dto() for doc in contract_documents]
    return {**project_contract[0].get_dto(), 'documents': documents}


def set_user_role_contract(contract_id: int, user_id: int, role_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectContractsRole.get_or_none(ProjectContractsRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    contract = ProjectContracts.get_or_none(ProjectContracts.id == contract_id)
    if not contract:
        raise ApiError.BadRequest('Contract not found')

    user_role = ProjectContractsUserRole.get_or_none(user=user, role=role, contract=contract)
    if user_role:
        raise ApiError.BadRequest('User has already been assigned to this role')

    project_contract_user_role = ProjectContractsUserRole(user=user, role=role, contract=contract)
    project_contract_user_role.save()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def remove_user_role_contract(contract_id: int, user_id: int, role_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ApiError.BadRequest('User not found')

    role = ProjectContractsRole.get_or_none(ProjectContractsRole.id == role_id)
    if not role:
        raise ApiError.BadRequest('Role not found')

    contract = ProjectContracts.get_or_none(ProjectContracts.id == contract_id)
    if not contract:
        raise ApiError.BadRequest('Contract not found')

    user_role = ProjectContractsUserRole.get_or_none(user=user, role=role, contract=contract)
    if not user_role:
        raise ApiError.BadRequest('User has already been assigned to this role')

    ProjectContractsUserRole.delete().where(ProjectContractsUserRole.id == user_role).execute()

    return {
        'id': user.id,
        'fullname': f'{user.lastname} {user.firstname} {user.surname}',
        'role': role.get_dto()
    }


def edit_stage(contract_id: int, status: str):
    contract = ProjectContracts.get_or_none(ProjectContracts.id == contract_id)
    if not contract:
        raise ApiError.BadRequest('Contract not found')

    if status not in contracts_status_list:
        ApiError.BadRequest('Status not found')

    contract.status = status
    contract.save()

    contract_documents = ProjectContractsDocument.fetch(ProjectContractsDocument.contract == contract_id)
    documents = [doc.get_dto() for doc in contract_documents]
    return {**contract.get_dto(), 'documents': documents}


def get_roles():
    return [role.get_dto() for role in ProjectContractsRole.select()]


def save_file(file: FileStorage, contract_id: int, file_type: str):
    contract = ProjectContracts.get_or_none(id=contract_id)
    if not contract:
        raise ApiError.BadRequest('Contract not found')

    file = file_service.save_file(file)

    document = ProjectContractsDocument(
        contract=contract,
        file=file,
        type=file_type
    )
    document.save()

    return document.get_dto()


def remove_file(file_id: str, contract_id: int):
    document = ProjectContractsDocument.get_or_none(contract=contract_id, file=file_id)
    if not document:
        raise ApiError.BadRequest('File not found')

    ProjectContractsDocument.delete().where(ProjectContractsDocument.id == document).execute()

    return document.get_dto()
