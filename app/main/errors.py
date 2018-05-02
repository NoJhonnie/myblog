# coding=utf-8
from flask import render_template



# errorhandler 用于处理被导入中的错误，即蓝本中的错误
# 该处使用 app_errorhandler 来注册程序全局的错误处理
from app.main import main


@main.app_errorhandler(400)
def page_not_found(e):
    return render_template('404.html'), 400


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
