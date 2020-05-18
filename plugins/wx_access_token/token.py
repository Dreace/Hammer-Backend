import json
import time

import requests
from flask_jwt import jwt_required

from global_config import wx_appid, wx_secret
from utils.check_authority import permission_required
from utils.redis_connections import redis_token
from utils.sql_helper import SQLHelper
from . import api


@api.route('/<worker_name>')
@jwt_required()
@permission_required(['wx_token'])
def get_access_token(worker_name: str):
    code = 0
    message = ""
    token_info = redis_token.get('token')
    if token_info:
        token_info = json.loads(token_info)
    if not token_info or token_info['expires_at'] - int(time.time()) < 600:  # expires in 10m
        token_info = {}
        token_data = requests.get(
            'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
                wx_appid, wx_secret)).content.decode()
        token_data_json: dict = json.loads(token_data)
        if 'errcode' in token_data_json:
            return {code: 500, message: '无法获取 access_token'}, 500
        token_info['token'] = token_data_json['access_token']
        token_info['expires_at'] = int(time.time()) + int(token_data_json['expires_in'])
        redis_token.set('token', json.dumps(token_info), ex=7200)
    sql = 'REPLACE INTO `worker_access`(worker_name, last_request_time) values (%s, %s)'
    SQLHelper.fetch_one(sql, (worker_name, (time.time())))
    return {
        'code': 0,
        'data': token_info
    }
