import datetime

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
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    classes = db.relationship('ClassModel', secondary=userClass, backref=db.backref('students'), lazy='dynamic')

class ClassModel(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.DateTime, nullable=False)
    videos = db.relationship('VideoModel', backref='classs')

class VideoModel(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    route = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

def create_app(app):
    db.init_app(app)
    return app