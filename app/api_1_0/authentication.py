# coding=utf-8
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from app.api_1_0 import api
from app.api_1_0.errors import forbidden, unauthorized
from app.models import AnonymousUser, User

auth = HTTPBasicAuth()

# 验证回调函数将认证的用户保存在全局对象 g 中
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

# 生成认证令牌 该令牌也要添加到 api 蓝本中
@api.route('/token/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('无效认证')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration':3600})

# flask_HTTPAuth 错误处理程序
@auth.error_handler
def auth_error():
    return unauthorized('无效认证')

# 所有 api 调用都先调用该函数，进行认证
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
        not g.current_user.confirmed:
        return forbidden('未注册用户')

# @api.route('/posts/1')
# def get_post():
#     pass
#     return jsonify({'post':'post1'})