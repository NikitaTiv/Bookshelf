import pytest

from webapp.utils.handler_files import allowed_file


@pytest.mark.parametrize(
    'elem1, elem2, expected_result',
    [
        ('.', 'txt', True),
        (':', 'txt', False),
        ('.', 'jpeg', False),
    ],
    ids=[
        'success_case',
        'file_with_wrong_separator',
        'file_with_wrong_extension',
    ], 
)
def test__allowed_file(create_name_extension, elem1, elem2, expected_result, app):
    with app.app_context():
        assert allowed_file(create_name_extension(elem1, elem2)) == expected_result
