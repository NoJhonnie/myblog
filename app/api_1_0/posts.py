# coding=utf-8
from flask import jsonify, request, g, url_for

from app import db
from app.api_1_0 import api
from app.api_1_0.decorators import permission_required
from app.api_1_0.errors import forbidden
from app.auth import auth
from app.models import Post, Permission

# 查询所有 blog 的 api
@api.route('/posts/')
def get_posts():
    posts = Post.query.all()
    return jsonify({'posts':[post.to_json() for post in posts]})

# 查询对应 id blog的api
@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

# 更新资源 blog
@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.quthor and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('无权限')
    post.body = request.json.get('body', post.body)
    post.title = request.json.get('title', post.title)
    db.session.add(post)
    return jsonify(post.to_json())

@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201,\
           {'Location': url_for('api.get_post', id=post.id, _external=True)}