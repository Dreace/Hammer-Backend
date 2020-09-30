from datetime import timedelta
from os import path

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt import JWT
from gevent.pywsgi import WSGIServer
from werkzeug import run_simple

from global_config import token_expire, secret_key, mysql_password, mysql_user, mysql_host
from models.sqlalchemy_db import db
from models.user import User
from startup import load_plugin
from utils.logger import root_logger

# from werkzeug import run_simple

app = Flask(__name__)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['SECRET_KEY'] = secret_key
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=token_expire)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_BINDS'] = {
    'nuc-info': 'mysql+pymysql://{}:{}@{}:3306/nuc_info'.format(mysql_user, mysql_password, mysql_host),
    'hammer': 'mysql+pymysql://{}:{}@{}:3306/hammer'.format(mysql_user, mysql_password, mysql_host)
}
# TODO JWT is valid for one hour, need to add refresh operation
# TODO May replace Flask-JWT to Flask-JWT-Extended
jwt = JWT(app, User.authenticate, User.identity)

db.init_app(app)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'code': 0,
        'data': {
            'access_token': access_token.decode('utf-8'),
        }
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code,
        'data': {
            "authority": ['guest'],
        },
    }), error.status_code


def initializer():
    plugins = load_plugin.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    for i in plugins:
        app.register_blueprint(i.api)


if __name__ == '__main__':
    initializer()
    run_simple('0.0.0.0', 10001, app,
               use_reloader=True, use_debugger=True, use_evalex=True)
    http_server = WSGIServer(('0.0.0.0', 10001), app, log=root_logger, error_log=root_logger)
    http_server.serve_forever()
