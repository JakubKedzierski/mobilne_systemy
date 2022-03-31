from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..app import db
from ..models import Offer
from ..user_errors import ValueNotSet

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


@bp.route('/offers/<int:id>', methods=['GET'])
def get_offer_by_id():
    offer_id = request.args.get('id')
    requested_offer = Offer.query.filter_by(id == offer_id).first()
    if requested_offer is None:
        return bad_request('Offer not found in database')

    offer_dict = {
        "offer" : requested_offer.to_dict()
    }

    return offer_dict

@bp.route('/offers/<int:id>', methods=['DELETE'])
def delete_offer_by_id(id):
    try:
        requested_offer = Offer.query.filter_by(id=id).first()
        db.session.delete(requested_offer)
        db.session.commit()
    except:
        return bad_request('Offer not found in database or database error')
    
    resp = jsonify(success=True)
    return resp
