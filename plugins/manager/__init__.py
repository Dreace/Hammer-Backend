from flask import Blueprint

api = Blueprint('%s_api' % __name__, __name__, url_prefix='/manager')

from .notice import *
from .authority import *
