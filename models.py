from app import db, app
from datetime import datetime
import os
from slugify import slugify
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'users.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey(
                           'role.id'), primary_key=True)
                       )


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey(
                         'post.id'), primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey(
                         'tag.id'), primary_key=True)
                     )

image_tags = db.Table('image_tags',
                      db.Column('image_id', db.Integer, db.ForeignKey(
                          'image.id'), primary_key=True),
                      db.Column('tag_id', db.Integer, db.ForeignKey(
                          'tag.id'), primary_key=True)
                      )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # create a String
    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % self.name


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    archive = db.Column(db.Boolean)

    def __repr__(self):
        return self.name

    def __init__(self, **kwargs):
        kwargs['archive'] = False
        kwargs['slug'] = slugify(kwargs.get('name'))
        super(Tag, self).__init__(**kwargs)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    alt = db.Column(db.String(80))
    tags = db.relationship('Tag', secondary=image_tags,
                           backref=db.backref('image', lazy='dynamic'),
                           cascade="save-update")
    archive = db.Column(db.Boolean)

    def path_to_save(self):
        path = str(os.path.join('static', 'upload', 'images'))
        return path

    def __repr__(self):
        return self.name

    def __init__(self, **kwargs):
        kwargs['archive'] = False
        super(Image, self).__init__(**kwargs)


class Gallery():
    pass


class Post(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(80), nullable=False)
    short_desc = db.Column(db.String(250), nullable=True)
    body = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.utcnow)
    archive = db.Column(db.Boolean)
    thumbnail = db.Column(db.String(80), nullable=True)
    video_url = db.Column(db.String(80), nullable=True)
    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('post', lazy='dynamic'),
                           cascade="save-update")

    def path_to_save(self):
        path = str(os.path.join('static', 'upload', 'posts', str(self.slug)))
        return path

    def __repr__(self):
        return '<Post %r>' % self.title

    def __init__(self, **kwargs):
        kwargs['archive'] = False
        kwargs['slug'] = slugify(kwargs.get('title'))
        super(Post, self).__init__(**kwargs)


'''
class SiteSet():
    site_logo = db.Column(db.String(80), nullable=True)
    site_name = db.Column(db.String(80), nullable=True)
    site_description = db.Column(db.String(250), nullable=True)
'''
