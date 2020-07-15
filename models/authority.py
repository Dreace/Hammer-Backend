from datetime import datetime

from models.sqlalchemy_db import db


class Authority(db.Model):
    __tablename__ = 'authority_test'
    __bind_key__ = 'hammer'
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(25))
    chinese_name = db.Column('chinese_name', db.TEXT)
    description = db.Column('description', db.TEXT)
    create_time = db.Column('create_time', db.TIMESTAMP, default=datetime.now)

    def serialize(self) -> dict:
        """
        serialize to dict

        :return: dict
        """
        return {
            "name": self.name,
            "chineseName": self.chinese_name,
            "description": self.description,
            "createTime": self.create_time.isoformat(),
        }
