# coding=utf-8
from datetime import datetime
from flask import render_template, redirect, url_for, session, flash, abort
from flask_login import login_required, current_user

from app import db
from app.decorators import admin_required, permission_required
from app.main import main
from app.main.forms import EditProfileForm, EditProfileAdminForm
from app.models import Permission, User, Role


@main.route('/', methods=['GET', 'POST'])
def index():
    from app.main.forms import NameForm
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # 视图函数index()注册的端点名为 main.index，简写为.index
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known', False), current_time = datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

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