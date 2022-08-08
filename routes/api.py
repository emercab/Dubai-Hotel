from flask import Blueprint, jsonify, request

bp_api = Blueprint("bp_api", __name__)

@bp_api.route('/api/clientes', methods=["post"])
def clientes_api():
    #print(request.get_json())
    print(len(request.json) > 0)

    return request.json['input1']
