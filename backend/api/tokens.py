from flask import request, jsonify
from functools import wraps
import jwt
from ..models import User
from flask import current_app as main_app
from .errors import bad_request

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return bad_request("Token not present. User is not authenticated.")
       try:
           data = jwt.decode(token, main_app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(email=data['email']).first()
       except:
           return bad_request("Token is invalid. User is not authenticated.")
 
       return f(current_user, *args, **kwargs)
   return decorator
