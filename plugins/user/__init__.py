from flask import Blueprint

api = Blueprint('%s_api' % __name__, __name__, url_prefix='/user')

from .user import *
