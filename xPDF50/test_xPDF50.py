from xPDF50 import is_valid, handle_uncharted, unpack
from prepare import extract_content, edit_tags
import pytest


def test_is_valid():
    with pytest.raises(SystemExit):
        is_valid('https://cpsc.yale.edu/')

    assert (
        is_valid('cs50.harvard.edu/python/2022/notes/0/')
        == 'https://cs50.harvard.edu/python/2022/notes/0'
    )


def test_unpack():
    with pytest.raises(SystemExit):
        unpack('https://cs50.harvard.edu/python/nom/nom')

    assert unpack('https://cs50.harvard.edu/python/2022/notes/0') == (
        'python',
        '2022',
        'lecture0',
    )


def test_handle_uncharted():
    assert handle_uncharted('https://cs50.harvard.edu/python/2022/project') == (
        '.....',
        '.....',
        'project',
    )


def test_edit_tags():
    assert edit_tags(
        '<div><p><img src="images/source.png" alt="Source"></p></div>',
        'https://cs50.harvard.edu/web/2020/notes/0',
        ) == (
            '<div><p><img src="https://cs50.harvard.edu/web/2020/notes/0/images/source.png"></p></div>'
        )