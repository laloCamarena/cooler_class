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

class1 = ClassModel(id=1, name='Matematicas 01', start_time=datetime.strptime('09:00', '%H:%M'), end_time=datetime.strptime('11:00', '%H:%M'), password=pwd_hash, admin=4)
class2 = ClassModel(id=2, name='Estructuras de datos', password=pwd_hash, admin=4)
class3 = ClassModel(id=3, name='Bases de datos', password=pwd_hash, admin=4)

post1 = PostModel(id=1, name='Tarea 01', description='Hacer un mapa conceptual sobre el teorema de pitagoras', class_id=1, informative=False)
post2 = PostModel(id=2, name='Tarea 02', description='Hacer una investigacion sobre estructuras de datos', class_id=1, informative=False)
post3 = PostModel(id=3, name='Tarea 01', description='Investigar que es SQL', class_id=2, informative=False)
post4 = PostModel(id=4, name='Aviso de suspencion de clases', description='El jueves no va a haber clases', class_id=3)
post5 = PostModel(id=5, name='Clase del jueves', description='La clase se aplazará una hora', class_id=1)
post6 = PostModel(id=6, name='Aviso!', description='Mañana no hay clases!', class_id=2)

file1 = FileModel(name='Gutierrez_Tarea 01', location='data/post_files/1/file1.pdf', user_id=1, post_id=1)
file2 = FileModel(name='Juan_Tarea_01', location='data/post_files/2/file2.pdf', user_id=1, post_id=2)
file5 = FileModel(name='Tarea 01', location='data/post_files/3/file3.pdf', user_id=2, post_id=3)
file6 = FileModel(name='Camarena_Tarea_01', location='data/post_files/1/file4.pdf', user_id=3, post_id=1)
file7 = FileModel(name='PerezTarea01', location='data/post_files/2/file5.pdf', user_id=3, post_id=2)

student1.classes.append(class1)
student1.classes.append(class3)
student2.classes.append(class2)
student2.classes.append(class3)
student3.classes.append(class1)

db.session.add_all([
    student1, student2, student3, student4,
    class1, class2, class3,
    post1, post2, post3, post4, post5, post6,
    file1, file2, file5, file6, file7
])
db.session.commit()