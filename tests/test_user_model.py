import time
import unittest
from datetime import datetime
from app import create_app, db
from app.models import User, Role, Permission, AnonymousUser, Follow


class UserModelTestCase(unittest.TestCase):
    # 尝试创建一个测试环境，测试配置创建程序，激活上下文，从而确保使用 current_app，使其像普通请求一样
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # 删除测试的数据库和上下文
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def test_password_setter(self):
    #     u = User(password = 'cat')
    #     self.assertTrue(u.password_hash is not None)
    #
    # def test_no_password_getter(self):
    #     u = User(password = 'cat')
    #     with self.assertRaises(AttributeError):
    #         u.password
    #
    # def test_password_verification(self):
    #     u = User(password = 'cat')
    #     self.assertTrue(u.verify_password('cat'))
    #     self.assertFalse(u.verify_password('dog'))
    #
    # def test_password_salts_are_random(self):
    #     u1 = User(password = 'cat')
    #     u2 = User(password = 'cat')
    #     self.assertTrue(u1.password_hash != u2.password_hash)
    #
    # def test_valid_confirmation_token(self):
    #     u = User(password = 'cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token()
    #     self.assertTrue(u.confirm(token))
    #
    # def test_invalid_confirmation_token(self):
    #     u1 = User(password='cat')
    #     u2 = User(password='dog')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     token = u1.generate_confirmation_token()
    #     self.assertFalse(u2.confirm(token))
    #
    # def test_expired_confirmation_token(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token(1)
    #     time.sleep(2)
    #     self.assertFalse(u.confirm(token))
    #
    # def test_valid_reset_password(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token()
    #     self.assertTrue(u.reset_password(token, 'dog'))
    #     self.assertTrue(u.verify_password('dog'))
    #
    # def test_invalid_reset_password(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token()
    #     self.assertFalse(u.reset_password(token + '1', 'dog'))
    #     self.assertTrue(u.verify_password('cat'))
    #
    # def test_valid_change_email(self):
    #     u = User(email='test@test.com',password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     token = u.generate_confirmation_token(new_email='test1@test.com')
    #     self.assertTrue(u.change_email(token))
    #     self.assertTrue(u.email == 'test1@test.com')
    #
    # def test_invalid_change_email(self):
    #     u1 = User(email='jack@test.com',password='cat')
    #     u2 = User(email='susan@test.com', password='dog')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     token = u1.generate_confirmation_token(new_email='jack1@test.com')
    #     self.assertFalse(u2.change_email(token))
    #     self.assertTrue(u2.email == 'susan@test.com')
    #
    # def test_unique_email(self):
    #     u1 = User(email='jack2@test.com', password='cat')
    #     u2 = User(email='susan2@test.com', password='dog')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     token = u2.generate_confirmation_token(new_email='jack2@test.com')
    #     self.assertFalse(u2.change_email(token))
    #     self.assertTrue(u2.email == 'susan2@test.com')
    #
    # def test_roles_and_permissions(self):
    #     Role.insert_roles()
    #     u = User(email='john@test.com', password='cat')
    #     self.assertTrue(u.can(Permission.WRITE_ARTICLES))
    #     self.assertFalse(u.can(Permission.MODERATE_COMMENTS))
    #
    # def test_user_role(self):
    #     u = User(email='john@example.com', password='cat')
    #     self.assertTrue(u.can(Permission.FOLLOW))
    #     self.assertTrue(u.can(Permission.COMMENT))
    #     self.assertTrue(u.can(Permission.WRITE_ARTICLES))
    #     self.assertFalse(u.can(Permission.MODERATE_COMMENTS))
    #     self.assertFalse(u.can(Permission.ADMINISTER))

    def test_moderator_role(self):
        r = Role.query.filter_by(name='Moderator').first()
        u = User(email='john5@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertTrue(u.can(Permission.MODERATE_COMMENTS))
        self.assertFalse(u.can(Permission.ADMINISTER))


    def test_administrator_role(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='johnadmin@example.com', password='cat', role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertTrue(u.can(Permission.MODERATE_COMMENTS))
        self.assertTrue(u.can(Permission.ADMINISTER))

    # def test_anonymous_user(self):
    #     u = AnonymousUser()
    #     self.assertFalse(u.can(Permission.FOLLOW))
    #     self.assertFalse(u.can(Permission.COMMENT))
    #     self.assertFalse(u.can(Permission.WRITE_ARTICLES))
    #     self.assertFalse(u.can(Permission.MODERATE_COMMENTS))
    #     self.assertFalse(u.can(Permission.ADMINISTER))

    # def test_timestamps(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     self.assertTrue(
    #         (datetime.utcnow() - u.member_since).total_seconds() < 3)
    #     self.assertTrue(
    #         (datetime.utcnow() - u.last_seen).total_seconds() < 3)
    #
    # def test_ping(self):
    #     u = User(password='cat')
    #     db.session.add(u)
    #     db.session.commit()
    #     time.sleep(2)
    #     last_seen_before = u.last_seen
    #     u.ping()
    #     self.assertTrue(u.last_seen > last_seen_before)
    #
    # def test_gravatar(self):
    #     u = User(email='john@example.com', password='cat')
    #     with self.app.test_request_context('/'):
    #         gravatar = u.gravatar()
    #         gravatar_256 = u.gravatar(size=256)
    #         gravatar_pg = u.gravatar(rating='pg')
    #         gravatar_retro = u.gravatar(default='retro')
    #     self.assertTrue('https://secure.gravatar.com/avatar/' +
    #                     'd4c74594d841139328695756648b6bd6' in gravatar)
    #     self.assertTrue('s=256' in gravatar_256)
    #     self.assertTrue('r=pg' in gravatar_pg)
    #     self.assertTrue('d=retro' in gravatar_retro)

    def test_follows(self):
        u1 = User(email='johnf@example.com', password='cat')
        u2 = User(email='susanf@example.org', password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        timestamp_before = datetime.utcnow()
        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        timestamp_after = datetime.utcnow()
        self.assertTrue(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        f = u1.followed.all()[-1]
        self.assertTrue(f.followed == u2)
        self.assertTrue(timestamp_before <= f.timestamp <= timestamp_after)
        f = u2.followers.all()[-1]
        self.assertTrue(f.follower == u1)
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 0)
        self.assertTrue(u2.followers.count() == 0)
        self.assertTrue(Follow.query.count() == 0)
        u2.follow(u1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(Follow.query.count() == 0)



