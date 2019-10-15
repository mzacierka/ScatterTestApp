import os


class Config:
    # session secret key
    SECRET_KEY = os.urandom(12)
    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

