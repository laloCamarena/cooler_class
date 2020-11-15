import json
import datetime
from passlib.hash import pbkdf2_sha512
from cooler_class.database.database import *
from cooler_class.transmition.transmition import *

with open('../config.json') as f:
    config_file = json.load(f)
    db_user = config_file['DB_user']
    db_password = config_file['DB_password']
    db_name = config_file['DB_name']

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{db_user}:{db_password}@localhost:3306/{db_name}'
db.drop_all()
db.create_all()

pwd = '12345678'
pwd_hash = pbkdf2_sha512.encrypt(pwd)
student1 = UserModel(id=1, first_name='Eduardo', last_name ='Camarena', email='lalo@gmail.com', password=pwd_hash)
student2 = UserModel(id=2, first_name='Diego', last_name='Gozalez', email='diego@gmail.com', password=pwd_hash)
student3 = UserModel(id=3, first_name='Juan', last_name='Olvera', email='juan@gmail.com', password=pwd_hash)
student4 = UserModel(id=4, first_name='Pepe', last_name='Alvarez', email='pepe@gmail.com', user_type='teacher', password=pwd_hash)

class1 = ClassModel(id=1, name='Aprendizaje 101', start_time=datetime.time(hour=9), end_time=datetime.time(hour=11), password=pwd_hash, admin=4)
class2 = ClassModel(id=2, name='Matematicas de algo 101', password=pwd_hash, admin=4)
class3 = ClassModel(id=3, name='Aprender!', password=pwd_hash, admin=4)

post1 = PostModel(id=1, name='Post 1', description='Post1 description', class_id=1)
post2 = PostModel(id=2, name='Post 2', description='Post2 description', class_id=1)
post3 = PostModel(id=3, name='Post 3', description='Post3 description', class_id=2)
post4 = PostModel(id=4, name='Post 4', description='Post4 description', class_id=3)
post5 = PostModel(id=5, name='Post 5', description='Post5 description', class_id=1)
post6 = PostModel(id=6, name='Post 6', description='Post6 description', class_id=2)

file1 = FileModel(name='file1', location='./data/post_files/file1.pdf', user_id=1, post_id=1)
file2 = FileModel(name='file2', location='./data/post_files/file2.pdf', user_id=1, post_id=2)
file3 = FileModel(name='file3', location='./data/post_files/file3.pdf', user_id=1, post_id=5)
file4 = FileModel(name='file4', location='./data/post_files/file4.pdf', user_id=1, post_id=4)
file5 = FileModel(name='file5', location='./data/post_files/file5.pdf', user_id=2, post_id=3)
file6 = FileModel(name='file6', location='./data/post_files/file6.pdf', user_id=3, post_id=1)
file7 = FileModel(name='file7', location='./data/post_files/file7.pdf', user_id=3, post_id=2)

student1.classes.append(class1)
student1.classes.append(class3)
student2.classes.append(class2)
student2.classes.append(class3)
student3.classes.append(class1)

db.session.add_all([
    student1, student2, student3, student4,
    class1, class2, class3,
    post1, post2, post3, post4, post5, post6,
    file1, file2, file3, file4, file5, file6, file7
])
db.session.commit()