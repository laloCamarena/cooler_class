# built-ins
import json

# Pypi packages
from passlib.hash import pbkdf2_sha256
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

with open('../../../config.json') as f:
    config_file = json.load(f)
    db_user = config_file['DB_user']
    db_password = config_file['DB_password']

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{db_user}:{db_password}@localhost:3306/cooler_class'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

userClass = db.Table(
    'UserClass',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    classes = db.relationship('class', secondary=userClass, backref=db.backref('students'), lazy='dynamic')

class ClassModel(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    students = db.relationship('user', secondary=userClass, backref=db.backref('classes'), lazy='dynamic')
    videos = db.relationship('VideoModel', backref='class')

class VideoModel(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    def __repr__(self):
        return f'Video(name = {self.name}), views = {self.views}, likes = {self.likes}'

# Create the database it hasn't been created
if not db.engine.table_names(): # this just checks if theres any tables, if there are missing tables in the database you need to create them again
    db.create_all()

# video parsers definition
video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video is required', required=True)
video_put_args.add_argument('views', type=int, help='Views of the video is required', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video')
video_update_args.add_argument('views', type=int, help='Views of the video')

video_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer
}

active_streams = []

class Video(Resource):
    @marshal_with(video_resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Could not find a video with that id')
        return result

    @marshal_with(video_resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args() # returns the data that was sent from tne user
        video = VideoModel(name=args['name'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(video_resource_fields)
    def patch(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exist')
        new_values = video_update_args.parse_args()
        for key, value in new_values.items():
            if value:
                setattr(result, key, value)
        db.session.add(result)
        db.session.commit()
        return result, 201

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exists')
        db.session.delete(result)
        db.session.commit()
        return '', 204

api.add_resource(Video, '/class/archive/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)