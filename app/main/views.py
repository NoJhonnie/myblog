# coding=utf-8
from datetime import datetime
from flask import render_template, redirect, url_for, session, flash, abort, request, current_app
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required, permission_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm, PostForm
from app.models import Permission, User, Role, Post


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )

    if form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body = form.body.data, author = current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = pagination.items
    return render_template('index.html', form=form, posts = posts, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    print(posts)
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('您的资料已更新')
        return redirect(url_for('.user', username = current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('您的资料已更新')
        return redirect(url_for('.user', username = user.username))
    form.name.data = user.name
    form.username.data = user.username
    form.email.data = user.email
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('文章已经更新')
        return redirect(url_for('.post', id=post.id))
    print(post.body_html,"+"*10,post.body)
    if post.body == '' or post.body is None:
        form.body.data=post.body_html
    else:
        form.body.data=post.body
    return render_template('edit_post.html', form=form)

@main.route('/admin')
@login_required
@admin_required
def for_admin():
    return 'admins page'

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderator():
    return 'comment moderator page!'