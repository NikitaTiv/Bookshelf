import pytest

from webapp.utils.handler_files import checks_available_format


@pytest.mark.parametrize(
    'string, expected_result',
    [
        ('text.txt', True),
        ('text:txt', False),
        ('text.jpeg', False),
    ],
    ids=[
        'success_case',
        'file_with_wrong_separator',
        'file_with_wrong_extension',
    ],
)
def test__checks_available_format(string, expected_result, app):
    assert checks_available_format(string) == expected_result
