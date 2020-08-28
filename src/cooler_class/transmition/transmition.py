# To run the app server you need to import this file to a script: from cooler_class.transmition import transmition
# you need to set the database: transmition.app.config['SQLALCHEMY_DATABASE_URI'] = {your_database}
# then you can run the server as transmition.app.run()

# built-ins
import time

# Pypi/local packages
import cv2
from passlib.hash import pbkdf2_sha512
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from cooler_class.database.database import *

app = Flask(__name__)
app = create_app(app)
app.app_context().push()
CORS(app)
api = Api(app)

# login parser definition
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str)
login_parser.add_argument('password', type=str)

class Login(Resource):
    def post(self):
        request.get_json()
        args = login_parser.parse_args()
        email = args['email']
        pwd = args['password']
        result = UserModel.query.filter_by(email=email).first()
        if result:
            if pbkdf2_sha512.verify(pwd, result.password):
                return {'name': result.name}, 201
            else:
                return 204
        else:
            return 204

# register parser definition
register_parser = reqparse.RequestParser()
register_parser.add_argument('name', type=str)
register_parser.add_argument('email', type=str)
register_parser.add_argument('password', type=str)

class Register(Resource):
    def post(self):
        request.get_json()
        args = register_parser.parse_args()
        name = args['name']
        email = args['email']
        pwd = args['password']
        if not UserModel.query.filter_by(email=email).first():
            pwd_hash = pbkdf2_sha512.encrypt(pwd)
            user = UserModel(name=name, email=email, password=pwd_hash)
            db.session.add(user)
            db.session.commit()
            return 201
        else:
            return 204


# register parser definition
addVideo_parser = reqparse.RequestParser()
addVideo_parser.add_argument('name', type=str, required=True)
addVideo_parser.add_argument('description', type=str)

class AddVideo(Resource):
    def post(self, class_id):
        request.get_json()
        args = addVideo_parser.parse_args()
        name = args['name']
        descrption = args['description']
        video = VideoModel(name=name, descrption=descrption, class_id=class_id)
        db.session.add(video)
        db.session.commit()
        return 201

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

    def process_video(self, video_route, fps):
        cap = cv2.VideoCapture(video_route)
        # read until eof
        while cap.isOpened():
            # get video frame by frame
            ret, img = cap.read()
            if ret:
                img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
                frame = cv2.imencode('jpg', img)[1].tobytes()
                yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                time.sleep(1 / fps)
            else:
                break

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(AddVideo, '/class/<int:class_id>/add_video/')
api.add_resource(Video, '/watch/<int:video_id>')