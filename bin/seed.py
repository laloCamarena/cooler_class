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
student1 = UserModel(first_name='Eduardo', last_name ='Camarena', email='lalo@gmail.com', password=pwd_hash)
student2 = UserModel(first_name='Diego', last_name='Gozalez', email='diego@gmail.com', password=pwd_hash)
student3 = UserModel(first_name='Juan', last_name='Olvera', email='juan@gmail.com', password=pwd_hash)
student4 = UserModel(first_name='Pepe', last_name='Alvarez', email='pepe@gmail.com', user_type='teacher', password=pwd_hash)

class1 = ClassModel(name='Aprendizaje 101', start_time=datetime.time(hour=9), end_time=datetime.time(hour=11), password=pwd_hash)
class2 = ClassModel(name='Matematicas de algo 101', password=pwd_hash)
class3 = ClassModel(name='Aprender!', password=pwd_hash)

student1.classes.append(class1)
student1.classes.append(class3)
student2.classes.append(class2)
student2.classes.append(class3)
student3.classes.append(class1)
student4.classes.append(class2)

db.session.add(class1)
db.session.add(class2)
db.session.add(class3)
db.session.add(student1)
db.session.add(student2)
db.session.add(student3)
db.session.add(student4)
db.session.commit()