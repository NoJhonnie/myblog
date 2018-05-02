import unittest
from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    # 尝试创建一个测试环境，测试配置创建程序，激活上下文，从而确保使用 current_app，使其像普通请求一样
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    #删除测试的数据库和上下文
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])