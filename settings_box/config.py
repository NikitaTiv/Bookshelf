from datetime import timedelta
from dotenv import load_dotenv
import os
from typing import Mapping, Any

load_dotenv()


def get_config() -> Mapping[str, Any]:
    return {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI'),
        'REMEMBER_COOKIE_DURATION': timedelta(days=180),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'ALLOWED_EXTENSIONS': {'txt'},
        'UPLOAD_FOLDER': os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '..', 'upload',
        ),
    }
