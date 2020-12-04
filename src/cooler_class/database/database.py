# built-ins
import datetime

# Pypi/local packages
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

userClass = db.Table(
    'UserClass',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), nullable=False)
)

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='student')
    password = db.Column(db.String(200), nullable=False)
    files = db.relationship('FileModel', backref='user')
    classes = db.relationship('ClassModel', secondary=userClass, backref=db.backref('students'), lazy='dynamic')

class ClassModel(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    days = db.Column(db.String(50), nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    videos = db.relationship('VideoModel', backref='classs')
    posts = db.relationship('PostModel', backref='classs')

class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    informative = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    files = db.relationship('FileModel', backref='post')

class FileModel(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class VideoModel(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    route = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

def add_db(app):
    db.init_app(app)
    return app