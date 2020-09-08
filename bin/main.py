# built-ins
import json

# Pypi packages
from cooler_class.transmition import transmition
from cooler_class.database import database

# you need to create a config.json file in the root of the project to store the user and password of the database
with open('../config.json') as f:
    config_file = json.load(f)
    db_user = config_file['DB_user']
    db_password = config_file['DB_password']
    db_name = config_file['DB_name']

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # this should only be used for tests
transmition.app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{db_user}:{db_password}@localhost:3306/{db_name}'

if __name__ == '__main__':
    # Create the database it hasn't been created
    if not database.db.engine.table_names(): # this just checks if theres any tables, if there are missing tables in the database you need to create them again
        transmition.db.create_all()
    transmition.app.run(debug=True)