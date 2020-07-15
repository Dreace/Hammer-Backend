import traceback

from flask import request, abort
from flask_jwt import jwt_required

from models.authority import Authority
from models.sqlalchemy_db import db
from utils.check_authority import permission_required
from . import api


@api.route('/authorities', methods=['GET'])
@jwt_required()
@permission_required(['admin'])
def manager_authority_fetch():
    return {
        'code': 0,
        'data': list(map(lambda x: x.serialize(), Authority.query.all()))
    }


@api.route('/authorities', methods=['POST'])
@jwt_required()
@permission_required(['admin'])
def manager_authority_create():
    post_data = request.get_json()
    try:
        authority = Authority.query.filter(Authority.name == post_data['name']).all()
        if authority:
            return {
                'code': -100,
                'message': '该类权限已存在'
            }
        authority = Authority(name=post_data["name"],
                              chinese_name=post_data["chineseName"],
                              description=post_data["description"])
        db.session.add(authority)
        db.session.commit()
    except TypeError as e:
        traceback.print_exc()
        abort(400)
    return {
        'code': 0,
    }


@api.route('/authorities/<int:authority_id>', methods=['DELETE'])
@jwt_required()
@permission_required(['admin'])
def manager_authority_delete(authority_id: int):
    authority: Authority = Authority.query.get(authority_id)
    if not authority:
        abort(404)
    db.session.delete(authority)
    db.session.commit()
    return {
        'code': 0,
    }


@api.route('/authorities/<int:authority_id>', methods=['PUT'])
@jwt_required()
@permission_required(['admin'])
def manager_authority_edit(authority_id: int):
    authority: Authority = Authority.query.get(authority_id)
    print(authority)
    if not authority:
        abort(404)
    post_data = request.get_json()
    try:
        authority.chinese_name = post_data["chineseName"]
        authority.description = post_data["description"]
    except TypeError:
        abort(400)
    db.session.commit()
    return {
        'code': 0,
    }
