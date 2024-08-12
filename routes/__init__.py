from .user import user
from .rights import rights
from .org_structure import org_structure
from .backpack import backpack
from .proposal import proposal
from .project import project
from .document_generation import generation
from .project_result import project_result
from .alert import alert
from .project_contract import project_contract
from .project_resources import project_resources
from .file import file
from .project_calendar_plan import project_calendar_plan
from .project_budget import budget
from .archive import archive
from .dashboard import dashboard


routes = [
    user.user_router,
    rights.rights_router,
    org_structure.org_structure_router,
    backpack.backpack_router,
    proposal.proposal_router,
    project.project_router,
    generation.generation_router,
    alert.alert_router,
    project_contract.project_contract_router,
    project_result.project_result_router,
    project_resources.project_resources_router,
    file.file_router,
    project_calendar_plan.project_calendar_plan_router,
    budget.budget_router,
    archive.archive_router,
    dashboard.dashboard_router,
]
