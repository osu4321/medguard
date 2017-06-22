import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'medguard1.db'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'heyoooooo'
SECRET_KEY = 'coolmancool'

# DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri (being used for SQLAlchemy)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
