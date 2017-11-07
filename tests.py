import pytest

from morizon.category import get_category


# , {'[number_of_rooms_from]': 2}     /?ps[number_of_rooms_from]=2
@pytest.mark.parametrize('args, filter, expected_value', [
    (('mieszkania', 'Warszawa', 'Stary Mokotów', 'do-wynajecia'), {'[number_of_rooms_from]': 2}, 'https://www.morizon.pl/do-wynajecia/mieszkania/warszawa/stary-mokotow/?ps[number_of_rooms_from]=2'),
])
def test_get_category(args, filter, expected_value):
    assert get_category(*args, **filter) == expected_value
