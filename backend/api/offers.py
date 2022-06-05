from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..app import db
from ..models import Offer, User, FavouriteOffers
from ..user_errors import ValueNotSet
from .tokens import token_required

@bp.route('/offers', methods=['GET'])
def get_offers():
    try:
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
    except:
        return bad_request('Database error')

@bp.route('/offers', methods=['POST'])
@token_required
def post_offer(current_user):
    data = request.get_json() or None
    if data is None:
        return bad_request('Lack of offer data')
    
    if 'offer' not in data:
        return bad_request('Lack of offer data')

    offer = Offer()
    try:
        offer.from_dict(data['offer'])
        offer.user_id = current_user.id 
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

@bp.route('/offers/favourite/<int:user_id>', methods=['GET'])
def get_favourite_offers(user_id):

    requested_user = User.query.filter_by(id=user_id).first()
    if requested_user is None:
        return bad_request('User not found in database')

    try:
        requested_offer_favourite = FavouriteOffers.query.filter_by(fav_user_id=user_id).all()
        part_offer_dict = []
        
        for fav_offer in requested_offer_favourite:
            requested_offer = Offer.query.filter_by(id=fav_offer.fav_offer_id).first()
            part_offer_dict.append(requested_offer.to_dict())
        
        offers_dict = {
            "offers" : part_offer_dict
        }

        return offers_dict
    except:
        return bad_request('Database error')
    
    return resp

@bp.route('/offers/favourite/<int:user_id>', methods=['POST'])
def post_favourite_offer(user_id):
    data = request.get_json() or None
    if data is None:
        return bad_request('Lack of offer data')
    
    if 'offerId' not in data:
        return bad_request('Lack of offer data')

    requested_user = User.query.filter_by(id=user_id).first()
    if requested_user is None:
        return bad_request('User not found in database')
    
    offer_id = data['offerId']
    requested_offer = Offer.query.filter_by(id=offer_id).first()
    if requested_offer is None:
        return bad_request('Offer not found in database')

    try:
        fav_offer = FavouriteOffers()
        fav_offer.fav_offer_id = offer_id
        fav_offer.fav_user_id = user_id
        db.session.add(fav_offer)
        db.session.commit()
    except ValueNotSet as error:
        return bad_request(str(error))
    except Exception as e:
        return bad_request('Problem occured while parsing json')
    
    resp = jsonify(success=True)
    return resp

@bp.route('/offers/favourite/<int:user_id>', methods=['DELETE'])
def delete_favourite_offer(user_id):
    data = request.get_json() or None
    if data is None:
        return bad_request('Lack of offer data')
    
    if 'offerId' not in data:
        return bad_request('Lack of offer data')

    requested_user = User.query.filter_by(id=user_id).first()
    if requested_user is None:
        return bad_request('User not found in database')
    
    offer_id = data['offerId']
    requested_offer = Offer.query.filter_by(id=offer_id).first()
    if requested_offer is None:
        return bad_request('Offer not found in database')

    try:
        requested_offer_favourite = FavouriteOffers.query.filter_by(fav_offer_id=offer_id).first()
        if requested_offer_favourite is not None:
            db.session.delete(requested_offer_favourite)
            db.session.commit()
        else:
            return bad_request('Favourite offer not found')
    except ValueNotSet as error:
        return bad_request(str(error))
    except Exception as e:
        return bad_request('Problem occured while parsing json')
    
    resp = jsonify(success=True)
    return resp
