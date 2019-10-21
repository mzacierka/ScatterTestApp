#EXAMPLE CONFIG FILE - INPUT YOUR OWN DATABASE INFO
import os

class Config:
    # session secret key
    SECRET_KEY = os.urandom(12)
    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    DB_USER = ""
    DB_PASS = ""

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASS + [URL_OF_DB]

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
