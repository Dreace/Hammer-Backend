import secrets
from datetime import datetime

from flask import request, abort
from flask_jwt import jwt_required

from models.insider import Insider
from models.sqlalchemy_db import db
from utils.check_authority import permission_required
from . import api


@api.route('/insiders', methods=['GET'])
@jwt_required()
@permission_required(['admin'])
def manager_insider_fetch():
    return {
        'code': 0,
        'data': list(map(lambda x: x.serialize(), Insider.query.all()))
    }


@api.route('/insiders', methods=['POST'])
@jwt_required()
@permission_required(['admin'])
def manager_insider_create():
    post_data = request.get_json()
    key = secrets.token_hex(10)
    try:
        insider = Insider(open_id=post_data['openId'],
                          key=key,
                          expire_at=datetime.fromtimestamp(int(post_data['expireAt']) / 1000),
                          status=int(post_data['status']))
        db.session.add(insider)
        db.session.commit()
    except TypeError:
        abort(400)
    return {
        'code': 0,
        'data': key
    }


@api.route('/insiders/<string:open_id>', methods=['DELETE'])
@jwt_required()
@permission_required(['admin'])
def manager_insider_delete(open_id: str):
    insider: Insider = Insider.query.get(open_id)
    if not insider:
        abort(404)
    db.session.delete(insider)
    db.session.commit()
    return {
        'code': 0,
    }


@api.route('/insiders/<string:open_id>', methods=['PUT'])
@jwt_required()
@permission_required(['admin'])
def manager_insider_edit(open_id: str):
    insider: Insider = Insider.query.get(open_id)
    if not insider:
        abort(404)
    post_data = request.get_json()
    try:
        insider.expire_at = datetime.fromtimestamp(int(post_data['expireAt']) / 1000),
        insider.status = post_data['status']
    except TypeError:
        abort(400)
    db.session.commit()
    return {
        'code': 0,
    }
