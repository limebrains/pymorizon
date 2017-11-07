import pytest

from morizon.category import get_category, get_max_page


# , {'[number_of_rooms_from]': 2}     /?ps[number_of_rooms_from]=2
from morizon.utils import get_url


@pytest.mark.parametrize('args, filter, expected_value', [
    (('mieszkania', 'Warszawa', 'Stary Mokotów', 'do-wynajecia'), {'[number_of_rooms_from]': 2, '[number_of_rooms_to]': 4}, 'https://www.morizon.pl/do-wynajecia/mieszkania/warszawa/stary-mokotow/?ps[number_of_rooms_from]=2&ps[number_of_rooms_to]=4'),
])
def test_get_url(args, filter, expected_value):
    assert get_url(*args, **filter) == expected_value


def test_get_max_page(url='https://www.morizon.pl/nieruchomosci/gdynia/witomino/'):
    assert get_max_page(url) == 4
