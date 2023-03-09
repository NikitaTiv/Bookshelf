from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
REMEMBER_COOKIE_DURATION = timedelta(days=180)
SQLALCHEMY_TRACK_MODIFICATIONS = False
ALLOWED_EXTENSIONS = {'txt'}
