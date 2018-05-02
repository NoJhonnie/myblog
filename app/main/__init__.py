from flask import Blueprint

main = Blueprint('main', __name__)

# 避免循环导入，同时将错误处理和路由函数与蓝图关联起来
from . import views, errors