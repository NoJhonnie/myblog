# coding=utf-8
from datetime import datetime
from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Comment, Tag

fake = Faker(locale='zh-CN')
def users(count=100):
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='123456',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    user_count = User.query.count()
    tag_count = Tag.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        t = Tag.query.offset(randint(0, tag_count-1)).first()
        p = Post(body_html=fake.text(),
                 title=fake.sentence(),
                 timestamp=fake.date_time_between(start_date=u.member_since),
                 author=u,
                 tags = [t])
        db.session.add(p)
    db.session.commit()

def comments(count=100):
    user_count = User.query.count()
    post_count = Post.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post.query.offset(randint(0, post_count - 1)).first()
        c = Comment(body_html=fake.sentence(),
                    timestamp=fake.date_time_between(start_date=max(u.member_since,p.timestamp)),
                    author = u,
                    post = p)
        db.session.add(c)
    db.session.commit()

def tags(count=10):
    for i in range(count):
        t = Tag(name=fake.word())
        db.session.add(t)
    db.session.commit()


