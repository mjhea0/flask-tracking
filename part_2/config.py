import os
import sqlite3

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False



ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'SecretKeyForSessionSigning'

THREADS_PER_PAGE = 8

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess"

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'blahblahblahblahblahblahblahblahblah'
RECAPTCHA_PRIVATE_KEY = 'blahblahblahblahblahblahprivate'
RECAPTCHA_OPTIONS = {'theme': 'white'}

DATABASE = 'test.db'

DATABASE_PATH = os.path.join(_basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH