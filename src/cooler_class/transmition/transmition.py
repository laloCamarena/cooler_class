# To run the app server you need to import this file to a script: from cooler_class.transmition import transmition
# you need to set the database: transmition.app.config['SQLALCHEMY_DATABASE_URI'] = {your_database}
# then you can run the server as transmition.app.run()

# built-ins
import time

# Pypi/local packages
import cv2
import io
import base64
from cv2 import data
import numpy as np
from PIL import Image
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from passlib.hash import pbkdf2_sha512
from cooler_class.database import database
# from cooler_class.model.model import MODEL, CLASS_NAMES
# from cooler_class.model.visualize import display_instances

app = Flask(__name__)
app = database.add_db(app)
app.app_context().push()
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# login parser definition
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str)
login_parser.add_argument('password', type=str)


user_resource_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'user_type': fields.String
}

class Login(Resource):
    @marshal_with(user_resource_fields)
    def post(self):
        request.get_json()
        args = login_parser.parse_args()
        email = str(args['email'])
        pwd = str(args['password'])
        result = database.UserModel.query.filter_by(email=email).first()
        if not result:
            return '',204
        elif not pbkdf2_sha512.verify(pwd, result.password):
            return '',204
        return result, 201

# register parser definition
register_parser = reqparse.RequestParser()
register_parser.add_argument('firstName', type=str)
register_parser.add_argument('lastName', type=str)
register_parser.add_argument('email', type=str)
register_parser.add_argument('password', type=str)
register_parser.add_argument('userType', type=str)

class Register(Resource):
    def post(self):
        request.get_json()
        args = register_parser.parse_args()
        first_name = str(args['firstName'])
        last_name = str(args['lastName'])
        email = str(args['email'])
        pwd = str(args['password'])
        user_type = str(args['userType'])
        if not database.UserModel.query.filter_by(email=email).first():
            pwd_hash = pbkdf2_sha512.encrypt(pwd)
            user = database.UserModel(
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=user_type,
                password=pwd_hash
            )
            save_to_db(user)
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
        name = str(args['name'])
        descrption = args['description']
        video = database.VideoModel(name=name, descrption=descrption, class_id=class_id)
        save_to_db(video)
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
        result = database.VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Could not find a video with that id')
        return result

    @marshal_with(video_resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args() # returns the data that was sent from tne user
        video = database.VideoModel(name=args['name'], views=args['views'])
        save_to_db(video)
        return video, 201

    @marshal_with(video_resource_fields)
    def patch(self, video_id):
        result = database.VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exist')
        new_values = video_update_args.parse_args()
        for key, value in new_values.items():
            if value:
                setattr(result, key, value)
        save_to_db(result)
        return result, 201

    def delete(self, video_id):
        result = database.VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video does not exists')
        database.db.session.delete(result)
        database.db.session.commit()
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

enroll_post_args = reqparse.RequestParser()
enroll_post_args.add_argument('student_id', type=int, help='Student ID is required', required=True)
enroll_post_args.add_argument('password', type=str, help='Password is required', required=True)
class Enroll(Resource):
    def post(self, class_id):
        request.get_json()
        args = enroll_post_args.parse_args()
        student_id = int(args['student_id'])
        password = str(args['password'])
        result = database.ClassModel.query.filter_by(id=class_id).first()
        if result.password != password:
            abort(204, message='Class password is incorrect')
        database.db.session.execute(database.userClass.insert().values(class_id=class_id, user_id=student_id))
        database.db.commit()
        return 201

class_data_post_args = reqparse.RequestParser()
class_data_post_args.add_argument('user_id', type=int, required=True)
class ClassData(Resource):
    def post(self):
        request.get_json()
        args = class_data_post_args.parse_args()


class UserData(Resource):
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        user = database.UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message='Could not find a user with that id')
        return user, 201

class UserClasses(Resource):
    def get(self, user_id):
        user = database.UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message='Could not find user')
        return_dicts = []
        for classs in user.classes:
            teacher = database.UserModel.query.filter_by(id=classs.admin).first()
            return_dicts.append({
                'id': classs.id,
                'name': classs.name,
                'days': classs.days,
                'startTime': str(classs.start_time),
                'endTime': str(classs.end_time),
                'teacher': f'{teacher.first_name} {teacher.last_name}'
            })
        return return_dicts, 201


classPost_post_args = reqparse.RequestParser()
classPost_post_args.add_argument('name', type=str, help='Post name is required', required=True)
classPost_post_args.add_argument('description', type=str, help='Post description is required', required=True)
class ClassPosts(Resource):
    def get(self, class_id):
        posts = database.PostModel.query.filter_by(class_id = class_id)
        return_dicts = []
        for post in posts:
            return_dicts.append({
                'id': post.id,
                'name': post.name,
                'description': post.description
            })
        return return_dicts, 201

    def post(self, class_id):
        request.get_json()
        args = enroll_post_args.parse_args()
        post_name = str(args['name'])
        post_description = str(args['description'])
        result = database.ClassModel.query.filter_by(id=class_id).first()
        if not result:
            abort(204, message='Class does not exist')
        post = database.PostModel(name=post_name, description=post_description)
        save_to_db(post)
        return {'success': True}, 201

    def patch(self, class_id):
        pass


post_files_post_args = reqparse.RequestParser()
post_files_post_args.add_argument('name', type=str, help='File name is required', required=True)
post_files_post_args.add_argument('attachment', type=str, help='Attatchment is required', required=True)

class PostFiles(Resource):
    def get(self, post_id, user_id):
        user = database.db.UserModel.query.filter_by(user_id=user_id)
        return_dicts = []
        if not user:
            abort(404, message='Could not find user')
        if user.user_type == 'student':
            f =  database.db.FileModel.query.filter_by(post_id=post_id, user_id=user_id)
            attachment = 'this should return the file as base64 string'
            return_dicts.append({'name': f.name, 'attachment': attachment})
        elif user.user_type == 'teacher':
            files = database.db.FileModel.query.filter_by(post_id=post_id)
            for f in files:
                #fix this shit
                attachment = 'this should return the file as base64 string'
                return_dicts.append({
                    'name': f.name,
                    'attatchment': attachment
                })
        return return_dicts, 201

    def post(self, post_id, user_id):
        request.get_json()
        args = post_files_post_args.parse_args()
        name = str(args['name'])
        attachment = str(args['attachment'])
        # pending: decode attachment str to pdf and save to storage
        f = database.FileModel(name=name, location=f'./data/post_files/{name}', user_id=user_id, post_id=post_id)
        save_to_db(f)
        return {'success': True}, 201

    def patch(self, post_id, user_id):
        pass

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(UserData, '/user/<int:user_id>')
api.add_resource(UserClasses, '/user/<int:user_id>/classes')
api.add_resource(Enroll, '/class/<int:class_id>/enroll')
api.add_resource(AddVideo, '/class/<int:class_id>/add_video/')
api.add_resource(Video, '/watch/<int:video_id>')
api.add_resource(ClassPosts, '/class/<int:class_id>/post')
api.add_resource(PostFiles, '/post/<int:post_id>/file/<int:user_id>')

#Socket communication
@socketio.on('stream')
def handle_frame(frame):
    frame_data = frame.split(',')
    # decode image to base64
    im_data = base64.b64decode(str(frame_data[1]))

    # reconstruct image as an numpy array
    img = Image.open(io.BytesIO(im_data))

    # convert image to cv2 image and convert it to BGR
    cv2_img = np.array(img)[:, :, ::-1]

    # analize image and create the new image that will be sent
    # results = MODEL.detect([cv2_img], verbose=0)
    # r = results[0]
    # cooler_image = display_instances(cv2_img.copy(), r['rois'], r['masks'], r['class_ids'], CLASS_NAMES, r['scores'])

    # encode image to base64
    buffer = cv2.imencode('.jpg', cv2_img)[1].tobytes()
    encoded_image = 'data:image/jpeg;base64,' + base64.b64encode(buffer).decode('utf-8')

    emit('get-stream', encoded_image, broadcast=True)

def save_to_db(data):
    database.db.session.add(data)
    database.db.session.commit()