import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Configures SQL Alchemy"""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # flask-login uses sessions which require a secret Key
