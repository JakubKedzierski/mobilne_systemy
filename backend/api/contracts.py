from . import bp
from flask import request, jsonify
from .errors import bad_request
from ..app import db
from ..models import Contract
from ..user_errors import ValueNotSet

@bp.route('/contracts', methods=['GET'])
def get_contracts():
    pass

@bp.route('/contracts/id', methods=['GET'])
def get_contract_by_id(id):
    pass

@bp.route('/contracts/filled', methods=['POST'])
def add_contract():
    data = request.get_json() or None
    if data is None:
        return bad_request('Lack of filled Contract data')

    contract = Contract()
    try:
        contract.from_dict(data)
        db.session.add(contract)
        db.session.commit()
    except ValueNotSet as error:
        return bad_request(str(error))
    #except Exception as e:
    #    return bad_request('Problem occured while parsing json')


    resp = jsonify(success=True) # response as pdf
    return resp