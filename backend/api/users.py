from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..models import User
from ..app import db
from ..user_errors import ValueNotSet


@bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if data is None:
        return bad_request('Lack of offer data')

    user = User()
    try:
        user.from_dict(data)
        db.session.add(user)
        db.session.commit()
    except ValueNotSet as error:
        return bad_request(str(error))
    except Exception as e:
        return bad_request('Problem occured while parsing json. Check if your email is unique or all data is provided')

    resp = jsonify(success=True)
    return resp


@bp.route('/login', methods=['GET'])
def login_user():
    data = request.get_json() or {}
    pass
