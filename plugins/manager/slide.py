from flask import request, abort
from flask_jwt import jwt_required

from models.slide import Slide
from models.sqlalchemy_db import db
from utils.check_authority import permission_required
from . import api


@api.route('/slides', methods=['GET'])
@jwt_required()
@permission_required(['admin'])
def manager_slide_fetch():
    return {
        'code': 0,
        'data': list(map(lambda x: x.serialize(), Slide.query.all()))
    }


@api.route('/slides', methods=['POST'])
@jwt_required()
@permission_required(['admin'])
def manager_slide_create():
    post_data = request.get_json()
    try:
        slide = Slide(index=post_data['index'],
                      name=post_data['name'],
                      image_url=post_data['imageUrl'],
                      content=post_data['content'])
        db.session.add(slide)
        db.session.commit()
    except TypeError:
        abort(400)
    return {
        'code': 0,
    }


@api.route('/slides/<int:slide_id>', methods=['DELETE'])
@jwt_required()
@permission_required(['admin'])
def manager_slide_delete(slide_id: int):
    slide: Slide = Slide.query.get(slide_id)
    if not slide:
        abort(404)
    db.session.delete(slide)
    db.session.commit()
    return {
        'code': 0,
    }


@api.route('/slides/<int:slide_id>', methods=['PUT'])
@jwt_required()
@permission_required(['admin'])
def manager_slide_edit(slide_id: int):
    slide: Slide = Slide.query.get(slide_id)
    if not slide:
        abort(404)
    post_data = request.get_json()
    try:
        slide.index = post_data['index'],
        slide.name = post_data['name'],
        slide.image_url = post_data['imageUrl'],
        slide.content = post_data['content']
    except TypeError:
        abort(400)
    db.session.commit()
    return {
        'code': 0,
    }
