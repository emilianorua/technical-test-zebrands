import os
from dotenv import load_dotenv


class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False