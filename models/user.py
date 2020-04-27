import hashlib
import json
import pickle

from global_config import token_expire
from utils.redis_connections import redis_user
from utils.sql_helper import SQLHelper


class User(object):
    def __init__(self, user_id: str, username: str, authority: list):
        """
        :param user_id: ID
        :param username: username
        :param authority: authority list
        """
        self.id = user_id
        self._username = username
        self._authority = authority

    @property
    def username(self) -> str:
        return self._username

    @property
    def authority(self) -> list:
        return self._authority

    def check_authority(self, authority_required: list) -> bool:
        """ check self._authority if in authority_required

        :param authority_required: authority list
        :return:
        """
        return len([i for i in self._authority if i in authority_required]) > 0

    @staticmethod
    def authenticate(username: str, password: str):
        """
        :param username:
        :param password:
        :return: User or None
        """
        sql = "SELECT * FROM `user` WHERE username=%s AND password_md5=%s"
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        user_info = SQLHelper.fetch_one(sql, (username, password_md5))
        if user_info:
            user = User(user_info['id'], user_info['username'], json.loads(user_info['authority']))
            redis_user.set(user_info["id"], pickle.dumps(user).decode('latin1'), ex=token_expire)
            return user

    @staticmethod
    def identity(payload):
        """
        :param payload:
        :return: User or None
        """
        user_id = payload['identity']
        user = redis_user.get(user_id)
        return pickle.loads(user.encode('latin1')) if user else None
