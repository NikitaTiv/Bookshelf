import pytest

from webapp import create_app


@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def create_name_extension():
    def create_name_extension_function(elem1, elem2):
        file_path = f'text{elem1}{elem2}'
        return file_path
    return create_name_extension_function
