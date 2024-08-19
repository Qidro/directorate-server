from pathlib import Path
from database import db
from flask import Flask
from flask_cors import CORS
from exceptions import ApiError
from routes import routes
from models import (
    User, Session, Right, UserRight, Department, Position, UserPosition, BackpackRole,
    BackpackUserRole, Backpack, ProposalExperts, Proposal, ProposalVerdicts, ProposalComment,
    Project, ProjectRole, ProjectUserRole, ProjectIndicators, ProjectIndicatorsRole,
    ProjectIndicatorsUserRole, ProjectIndicatorsValues, ProjectResults, ProjectResultsRoles, ProjectResultValues,
    ProjectResultsUserRole, Alert, ProjectContracts, ProjectContractsRole, ProjectContractsUserRole,
    ProjectContractsDocument, File, ProjectDocument, ProjectCalendarPlan, ProjectCalendarPlanCP,
    ProjectCalendarPlanResults, ProjectCalendarPlanRole, ProjectCalendarPlanUserRole, BackpackDocument, ProjectBudget,
    ProposalLog, UserLog, BackpackLog, ProjectLog, ProjectIndicatorsLog, ProjectResultsLog, ProjectCalendarPlanLog,
    ProjectContractsLog
)

import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, supports_credentials=True)

for route in routes:
    app.register_blueprint(route, url_prefix='/api')


@app.errorhandler(ApiError.ApiError)
def api_error(error):
    return error.message, error.status


@app.errorhandler(404)
def api_error(error):
    return 'Url not found', 404


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    with db:
        db.create_tables([
            User, Session, Right, UserRight, Department, Position, UserPosition, Backpack, BackpackRole,
            BackpackUserRole, Proposal, ProposalExperts, ProposalVerdicts, ProposalComment,
            ProjectResultsUserRole, Project, ProjectRole, ProjectUserRole, ProjectIndicators, ProjectIndicatorsRole,
            ProjectIndicatorsUserRole, ProjectIndicatorsValues, ProjectResults, ProjectResultsRoles,
            ProjectResultValues, Alert, ProjectContracts, ProjectContractsRole, ProjectContractsUserRole,
            ProjectContractsDocument, File, ProjectDocument, ProjectCalendarPlan, ProjectCalendarPlanCP,
            ProjectCalendarPlanResults, ProjectCalendarPlanRole, ProjectCalendarPlanUserRole,
            BackpackDocument, ProjectBudget, ProposalLog, UserLog, BackpackLog, ProjectLog, ProjectIndicatorsLog,
            ProjectResultsLog, ProjectCalendarPlanLog, ProjectContractsLog
        ])

    app.run(debug=os.environ.get('DEBUG') or False, port=os.environ.get('PORT'))
    #app.run(debug=os.environ.get('DEBUG') or False, port=os.environ.get('PORT'), ssl_context=('cert.pem', 'key.pem'))