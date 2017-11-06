import pytest

from morizon.category import get_category


@pytest.mark.parametrize('args, expected_value', [
    (('do-wynajecia', 'mieszkania' ,'warszawa', 'stary-mokotow'), 'url_wymagany'),
])
def test_get_category(args, expected_value):
    assert get_category(args) == expected_value
