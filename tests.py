# pytest tests.py  -vv --pdb --cov=morizon --cov-report=term-missing
import pytest
import sys

if sys.version_info < (3, 3):
    from mock import mock
else:
    from unittest import mock
from morizon.utils import *
from morizon.offer import *


@pytest.fixture
def offer_markup():
    with open('offer_source.htm', 'r') as page:
        page_markup = page.read()
    html_markup = BeautifulSoup(page_markup, "html.parser")
    return html_markup

@pytest.mark.parametrize('args, filter, expected_value', [
    (('mieszkania', 'Gdynia', 'Witomino Leśniczówka', 'do-wynajecia'), {'[number_of_rooms_from]': 2}, 'https://www.morizon.pl/do-wynajecia/mieszkania/gdynia/witomino-lesniczowka/?page=1&ps%5Bnumber_of_rooms_from%5D=2&'),
    (('domy', 'Warszawa', 'Śródmieście'), {'[number_of_rooms_from]': 4, }, 'https://www.morizon.pl/domy/warszawa/srodmiescie/?page=1&ps%5Bnumber_of_rooms_from%5D=4&'),
    (('działki', 'Opole'), {}, 'https://www.morizon.pl/dzialki/opole/?page=1&'),
    (('mieszkania', 'Szczecin', 'Pogodno', 'do-wynajecia'), {'[living_area_from]': 35,'[number_of_rooms_from]': 2}, 'https://www.morizon.pl/do-wynajecia/mieszkania/szczecin/pogodno/?page=1&ps%5Bliving_area_from%5D=35&ps%5Bnumber_of_rooms_from%5D=2&'),
])
def test_get_url(args, filter, expected_value):
    assert URL(*args, filters=filter).get_url() == expected_value


@pytest.mark.parametrize('url, city', [
    ('https://www.morizon.pl/nieruchomosci/gdynia/witomino/?page=1&', 'gdynia'),
    ('https://www.morizon.pl/do-wynajecia/mieszkania/warszawa/stary-mokotow/?page=1&ps%5Bnumber_of_rooms_from%5D=2&ps%5Bnumber_of_rooms_to%5D=4&', 'warszawa'),
])
def test_url_parsing(url, city):
    url_obj = URL.from_string(url)
    assert url_obj.city == city
    assert url_obj.get_url() == url


@pytest.mark.parametrize('text, expected_value', [
    ('ĄĆĘŁŃÓŚŹŻ', 'acelnoszz'),
    ('Zielona Góra', 'zielona-gora'),
    ('Świętojańska', 'swietojanska'),
    ('PrZykłaDowY tEXt', 'przykladowy-text')
])
def test_encode_text(text, expected_value):
    assert encode_text_to_url(text) == expected_value


def test_get_area(offer_markup):
    assert get_surface_for_offer(offer_markup) == 56.34


def test_get_floor(offer_markup):
    assert get_floor_for_offer(offer_markup) == 0


def test_get_price(offer_markup):
    assert get_price_for_offer(offer_markup) == 1600.0


def test_get_phone(offer_markup):
    assert get_phone_for_offer(offer_markup) == '508 861 700'


def test_get_voivodeship(offer_markup):
    assert get_voivodeship_for_offer(offer_markup) == 'zachodniopomorskie'


def test_get_images(offer_markup):
    images = get_images_for_offer(offer_markup)
    assert isinstance(images, list)
    for image in images:
        assert 'https://img' in image