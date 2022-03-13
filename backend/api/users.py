from backend.api import bp
from flask import request


@bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    pass


@bp.route('/login', methods=['GET'])
def login_user():
    data = request.get_json() or {}
    pass
