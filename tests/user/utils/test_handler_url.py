from dotenv import load_dotenv
import os

load_dotenv()

from webapp.utils.handler_url import get_connection_dsn


def test__get_connection_dsn__success_case():
    assert get_connection_dsn() == os.getenv('DB_URL_FOR_TEST')
