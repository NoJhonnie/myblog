from sqlite3 import OperationalError

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm
from app.email import send_email
from app.models import User
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
        except OperationalError as e:
            print(e)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('账号或密码错误！！！')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已退出")
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '激活您的账号', 'auth/email/confirm', user=user, token=token)
        flash('激活链接已发到您的邮箱里！')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您的账号已经激活！谢谢')
    else:
        flash('激活链接无效或已过期')

    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.before_app_request
def before_request():
    # print('1:',current_user.is_authenticated)
    # print('2:',current_user.confirmed)
    # print('3:',request.endpoint[:5])
    if current_user.is_authenticated and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '激活您的账号', 'auth/email/confirm', user=current_user, token=token)
    flash('新的激活链接已发到您的邮箱里！')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('您的密码已经修改')
            return redirect(url_for('main.index'))
        else:
            flash('当前密码错误')
    return render_template('auth/change_password.html', form=form)
