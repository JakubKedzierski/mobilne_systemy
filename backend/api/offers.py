from backend.api import bp
from flask import request


@bp.route('/offers', methods=['GET'])
def get_offers():
    pass


@bp.route('/offers/<int:id>', methods=['GET'])
def get_offer_by_id():
    pass
