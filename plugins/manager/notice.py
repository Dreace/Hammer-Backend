from flask import request, abort
from flask_jwt import jwt_required

from models.notice import Notice
from models.sqlalchemy_db import db
from utils.check_authority import permission_required
from . import api


@api.route('/notices', methods=['GET'])
@jwt_required()
@permission_required(['admin'])
def manager_notice_fetch():
    return {
        'code': 0,
        'data': list(map(lambda x: x.serialize(), Notice.query.all()))
    }


@api.route('/notices', methods=['POST'])
@jwt_required()
@permission_required(['admin'])
def manager_notice_create():
    post_data = request.get_json()
    try:
        notice = Notice(title=post_data["title"],
                        content=post_data["content"],
                        is_important=post_data["isImportant"],
                        is_stick=post_data["isStick"])
        db.session.add(notice)
        db.session.commit()
    except TypeError:
        abort(400)
    return {
        'code': 0,
    }


@api.route('/notices/<int:notice_id>', methods=['DELETE'])
@jwt_required()
@permission_required(['admin'])
def manager_notice_delete(notice_id: int):
    notice: Notice = Notice.query.get(notice_id)
    if not notice:
        abort(404)
    db.session.delete(notice)
    db.session.commit()
    return {
        'code': 0,
    }


@api.route('/notices/<int:notice_id>', methods=['PUT'])
@jwt_required()
@permission_required(['admin'])
def manager_notice_edit(notice_id: int):
    notice: Notice = Notice.query.get(notice_id)
    if not notice:
        abort(404)
    post_data = request.get_json()
    try:
        notice.title = post_data["title"]
        notice.content = post_data["content"]
        notice.is_important = post_data["isImportant"]
        notice.is_stick = post_data["isStick"]
    except TypeError:
        abort(400)
    db.session.commit()
    return {
        'code': 0,
    }
