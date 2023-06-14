import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-not-pass'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://@localhost/flask_db"
    MAILADRESS = ['testMail@example.com']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'secret_key'
    OAUTH_CREDENTIALS = {
        'vk': {
            'id': 'app_id',
            'secret': 'secret'
        }
    }
