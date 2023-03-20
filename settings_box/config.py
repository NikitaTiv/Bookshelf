from datetime import timedelta
from dotenv import load_dotenv
import os
from typing import Mapping, Any

from webapp.utils.handler_url import get_connection_dsn

load_dotenv()


def get_config() -> Mapping[str, Any]:
    return {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': get_connection_dsn(),
        'REMEMBER_COOKIE_DURATION': timedelta(days=180),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'ALLOWED_EXTENSIONS': {'txt'},
        'UPLOAD_FOLDER': os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '..', 'upload',
        ),
    }
