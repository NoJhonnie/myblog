import time
import unittest

from app import db
from app.models import User, Role, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
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

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='john@test.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
