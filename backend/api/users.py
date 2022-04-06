from . import bp
from flask import request, jsonify, session
from flask import current_app as main_app
from werkzeug.security import check_password_hash
import jwt
from .errors import bad_request
from ..models import User
from ..app import db
from ..user_errors import ValueNotSet


@bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    if data is None:
        return bad_request('Lack of user data')

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

    if data is None:
        return bad_request('Lack of user data')

    fields = ['email', 'password']
    for field in fields:
        if field not in data:
            return bad_request('Lack of user data')

    req_email = data['email']
    req_password = data['password']
    
    requested_user = User.query.filter_by(email = req_email).first()
    if requested_user is None:
        return bad_request('User not found in database')
    
    if not check_password_hash(requested_user.password, req_password):
        return bad_request('Wrong password')


    token = jwt.encode({'firstName' : requested_user.first_name, 'secondName' : requested_user.second_name, 'email':requested_user.email,
             'phone':requested_user.phone, 'address':requested_user.address}, main_app.config['SECRET_KEY'], "HS256")
    session[requested_user.id] = token 

    resp = jsonify(succes=True, token=token)
    return resp


# TEMP debug
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    try:
        requested_user =  User.query.filter_by(id=user_id).first()
        db.session.delete(requested_user)
        db.session.commit()
    except:
        return bad_request('User not found in database or database error')
    
    resp = jsonify(success=True)
    return resp
