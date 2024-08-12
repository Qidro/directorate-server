from flask import Blueprint, request, jsonify
from webargs import flaskparser
from routes.alert.fields import alert_model
from service import alert_service

alert_router = Blueprint('alert', __name__)


@alert_router.get('/alert')
def alert():
    alert = alert_service.get_alert()

    return jsonify(alert)


@alert_router.post('/alert/set')
def set_alert():
    data = flaskparser.parser.parse(alert_model, request)
    alert = alert_service.set_alert(data['text'])

    return jsonify(alert)

