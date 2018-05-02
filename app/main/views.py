# coding=utf-8
from datetime import datetime
from flask import render_template, redirect, url_for, session, flash
from app.main import main


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

@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
