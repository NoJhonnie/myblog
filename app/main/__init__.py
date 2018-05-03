from flask import Blueprint

from app.models import Permission

main = Blueprint('main', __name__)

# 避免循环导入，同时将错误处理和路由函数与蓝图关联起来
from . import views, errors

#为了避免每次调用 render_template多添加一个模板参加，使用上下文处理器
#即把 Permission 类加入到模板上下文中
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)