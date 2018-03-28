import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = False
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
SECRET_KEY = '87469976308fd14a2d0148247d441f2756b6176a'