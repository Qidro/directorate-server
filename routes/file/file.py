from flask import Blueprint, send_file
from service import file_service

file_router = Blueprint('file', __name__)


@file_router.get('/file/<file_id>')
def get_file(file_id):
    url, filename = file_service.get_file(file_id)
    return send_file(url, download_name=filename, as_attachment=True)
