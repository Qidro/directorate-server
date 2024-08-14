from datetime import datetime

from models import Project, ProjectUserRole, ProjectCalendarPlan, ProjectCalendarPlanUserRole, Backpack, Proposal, \
    ProposalVerdicts, ProjectLog


def get_common_dashboard(user, start_date: datetime.date, end_date: datetime.date):
    my_projects = Project.fetch(((Project.is_Archived == False) & (((Project.start_date >= start_date)
                 & (Project.start_date <= end_date)) | ((Project.creation_date >= start_date)
                 & (Project.creation_date <= end_date))) & (ProjectUserRole.user == user.id)))

    my_calendar_plan = ProjectCalendarPlan.fetch((((ProjectCalendarPlan.start_date_plan >= start_date)
                                                   & (ProjectCalendarPlan.start_date_plan <= end_date))
                                                  | ((ProjectCalendarPlan.end_date_plan >= start_date)
                                                     & (ProjectCalendarPlan.end_date_plan <= end_date)))
                                                 & (ProjectCalendarPlanUserRole.user == user.id)
                                                 & (Project.is_Archived == False))

    return {
        'projects': [project.get_dto() for project in my_projects],
        'calendar_plan': [calendar_plan.get_dto() for calendar_plan in my_calendar_plan]
    }


def get_advanced_dashboard(user, start_date: datetime.date, end_date: datetime.date):
    projects = Project.fetch(Project.creation_date <= end_date)

    project_count = len(projects)

    backpack_count = len(Backpack.fetch(Backpack.creation_date <= end_date))

    proposal_count = len(Proposal.fetch(Proposal.submission_date <= end_date))

    proposal_count_list_by_status = {
        'success': 0,
        'reject': 0,
        'archived': 0,
        'development': 0,
    }
    
    for status in ['SUCCESS', 'REJECT', 'ARCHIVED']:
        proposal_count_by_status = len(ProposalVerdicts.select().where((ProposalVerdicts.status == status)
                                                                     & (ProposalVerdicts.date >= start_date)
                                                                     & (ProposalVerdicts.date <= end_date))
                                     .group_by(ProposalVerdicts.project_proposal))

        proposal_count_list_by_status[status.lower()] += proposal_count_by_status

    proposal_count_list_by_status['development'] = proposal_count - proposal_count_list_by_status['success'] - proposal_count_list_by_status['reject']
    - proposal_count_list_by_status['archived']

    project_count_list_by_status = {
        'initiation': 0,
        'preparation': 0,
        'realization': 0,
        'completion': 0,
        'post_project_monitoring': 0,
        'archived': 0,
        'canceled': 0,
    }

    for status in ['INITIATION', 'PREPARATION', 'REALIZATION','COMPLETION', 'POST_PROJECT_MONITORING', 'ARCHIVED','CANCELED']:
        project_count_by_status = len(Project.select().where((Project.status == status)))
                                     #.group_by(Project.backpack))

        project_count_list_by_status[status.lower()] += project_count_by_status
    """
    for project in projects:
        logs = ProjectLog.fetch(
            condition=((ProjectLog.project == project.id)
                       & ((ProjectLog.action == 'CREATE_PROJECT') | (ProjectLog.action == 'UPDATE_STAGE'))
                       & (ProjectLog.date_change >= start_date) & ((ProjectLog.date_change_out < end_date)
                                                                   | (ProjectLog.date_change_out == None))),
            order_by=ProjectLog.id.desc(),
            limit=1
        )



        try:
            log = [log.get_dto() for log in logs][0]
            project_count_list_by_status[log['new_status'].lower()] += 1
        except:
            pass
        """

    return {
        'project_count': project_count,
        'backpack_count': backpack_count,
        'proposal_count': proposal_count,
        'proposal_count_list': proposal_count_list_by_status,
        'project_count_list': project_count_list_by_status
    }