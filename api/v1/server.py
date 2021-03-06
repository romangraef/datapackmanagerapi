from flask import Blueprint, jsonify, abort, make_response, request

from .db import Category, DataPack, User, Tag, TagRelation
from .util import model_paginator, query_paginator, ConstrainFailed, get_tags_for_datapack

bp = Blueprint("api v1", __name__)


@bp.errorhandler(ConstrainFailed)
def handler(e: ConstrainFailed):
    return make_response(jsonify({
        'error': {
            'description': e.description,
            'parameter': e.parameter,
            'reason': e.reason,
        }
    }), 404)


@bp.route('/version/')
def version():
    return jsonify({
        'version': '1.0.0',
        'deprecated': False,
    })


@bp.route('/list/categories/')
def list_categories():
    return model_paginator(Category, lambda cat: {
        'name': cat.name,
        'id': cat.id,
    })


@bp.route('/list/datapacks')
def list_datapacks():
    category = request.args.get('category', '')
    query = DataPack.select().join(User)
    if category != '':
        query = query.join(Category).where(DataPack.category.id == category)
    return query_paginator(query, lambda dp: {
        'name': dp.name,
        'id': dp.id,
        'description': dp.description,
        'tags': get_tags_for_datapack(dp),
        'author': dp.author.id,
        'likes': dp.likes,
        'dislikes': dp.dislikes,
        'downloads': dp.downloads,
        'views': dp.views,
        'category': dp.category.id,

    })


@bp.route('/<path:invalid_path>')
def invalid_path(invalid_path):
    abort(404)
