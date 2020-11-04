import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Config class for secret key for submitted form
class Config():
     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will nevr guess this....'
     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')\
         or 'sqlite:///' + os.path.join(basedir, 'app.db')
     SQLALCHEMY_TRACK_MODIFICATIONS = False
     IEX_TOKEN = os.environ.get('IEX_TOKEN')

     TEMPLATES_AUTO_RELOAD = True
    #  everytime there is a change to the app files, forces reload 