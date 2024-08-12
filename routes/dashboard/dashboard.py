from flask import Blueprint, jsonify
from decorators import login_required
from service import dashboard_service

dashboard_router = Blueprint('dashboard ', __name__)


@dashboard_router.get('/dashboard/<start_date>_<end_date>/common')
@login_required
def get_common_dashboard(user, start_date, end_date):
    dashboard = dashboard_service.get_common_dashboard(user, start_date, end_date)
    return jsonify(dashboard)


@dashboard_router.get('/dashboard/<start_date>_<end_date>/advanced')
@login_required
def get_advanced_dashboard(user, start_date, end_date):
    dashboard = dashboard_service.get_advanced_dashboard(user, start_date, end_date)
    return jsonify(dashboard)