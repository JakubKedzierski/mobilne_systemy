from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..app import db
from ..models import Offer
from ..user_errors import ValueNotSet
from .tokens import token_required

@bp.route('/offers', methods=['GET'])
def get_offers():
    requested_offers = Offer.query.all()
    if requested_offers is None:
        return bad_request('Offers not found in database')

    part_offer_dict = []
    for offer in requested_offers:
        part_offer_dict.append(offer.to_dict())
     

    offers_dict = {
        "offers" : part_offer_dict
    }

    return offers_dict

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
        return bad_request('Problem occured while parsing json')
        
    resp = jsonify(success=True)
    return resp


@bp.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer_by_id(offer_id):
    requested_offer = Offer.query.filter_by(id=offer_id).first()
    if requested_offer is None:
        return bad_request('Offer not found in database')

    offer_dict = {
        "offer" : requested_offer.to_dict()
    }

    return offer_dict

@bp.route('/offers/<int:offer_id>', methods=['DELETE'])
@token_required
def delete_offer_by_id(current_user, offer_id):
    try:
        requested_offer = Offer.query.filter_by(id=offer_id).first()
        if requested_offer is None:
            return bad_request('Offer not found in database')
        if requested_offer in current_user.offers:
            db.session.delete(requested_offer)
            db.session.commit()
        else:
            return bad_request('User not allowed to delete this offer')
    except:
        return bad_request('Database error')
    
    resp = jsonify(success=True)
    return resp
