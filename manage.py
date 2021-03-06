# coding=utf-8
import os
import pdb
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import db, create_app, faker
from app.models import User, Role, Post, Follow, Permission, Comment, Tag

app = create_app(os.environ.get('MYBLOG_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)

# pdb.set_trace()

def make_shell_context():

    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Tag=Tag, Comment=Comment, Follow=Follow, Permission=Permission, faker=faker)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 自定义命令
@manager.command
def test():
    '''单元测试'''
    import unittest
    # pdb.set_trace()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()


