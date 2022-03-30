from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..app import db
from ..models import Offer
from ..user_errors import ValueNotSet

@bp.route('/offers', methods=['GET'])
def get_offers():
    return {"check" : "works"}

@bp.route('/offers', methods=['POST'])
def post_offer():
    data = request.get_json() or None
    if data is None:
        return bad_request('Lack of offer data')
    
    if 'offer' not in data:
        return bad_request('Lack of offer data')

    offer = Offer()
    try:
        offer.from_dict(data['offer'])

# TO DO - add proper user
        offer.user_id = 1 
        db.session.add(offer)
        db.session.commit()
    except ValueNotSet as error:
        return bad_request(str(error))
    except Exception as e:
        return bad_request('Problem occured while parsing json\nMessage: ' + str(e))
    


        
    resp = jsonify(success=True)
    return resp
    


@bp.route('/offers/<int:id>', methods=['GET'])
def get_offer_by_id():
    pass
