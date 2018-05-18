# coding=utf-8
from flask import current_app
from itsdangerous import Serializer

from app import db

# User 模型的生成和验证认证令牌
class User(db.Model):

    #生成编码后的用户 id 字段值得签名令牌
    def genereate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expiration_in = expiration)
        return s.dumps({'id': self.id})

    #验证对应的用户
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])