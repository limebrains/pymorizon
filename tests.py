import pytest
import sys

import time
from bs4 import BeautifulSoup
if sys.version_info < (3, 3):
    from mock import mock
else:
    from unittest import mock
from morizon.utils import *
from morizon.offer import *


OFFER_URL = 'https://www.morizon.pl/oferta/wynajem-mieszkanie-sopot-wyscigi-wladyslawa-lokietka-58m2-mzn2028877346'


@pytest.fixture
def offer_markup():
    response = get_content_from_source(OFFER_URL)
    html_markup = BeautifulSoup(response.content, "html.parser")
    return html_markup

@pytest.mark.parametrize('args, filter, expected_value', [
    (('mieszkania', 'Gdynia', 'Witomino Leśniczówka', 'do-wynajecia'), {'[number_of_rooms_from]': 2}, 'https://www.morizon.pl/do-wynajecia/mieszkania/gdynia/witomino-lesniczowka/?page=1&ps%5Bnumber_of_rooms_from%5D=2&'),
    (('domy', 'Warszawa', 'Śródmieście'), {'[number_of_rooms_from]': 4, }, 'https://www.morizon.pl/domy/warszawa/srodmiescie/?page=1&ps%5Bnumber_of_rooms_from%5D=4&'),
    (('działki', 'Opole'), {}, 'https://www.morizon.pl/dzialki/opole/?page=1&'),
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

# @pytest.mark.parametrize('url, expected_values', [
#     ('https://www.morizon.pl/nieruchomosci/gdynia/witomino/', 4),
# ])
# def test_get_max_page(url, expected_values):
#     assert URL.from_string(url).max_num_of_pages() == expected_values


@pytest.mark.parametrize('text, expected_value', [
    ('ĄĆĘŁŃÓŚŹŻ', 'acelnoszz'),
    ('Zielona Góra', 'zielona-gora'),
    ('Świętojańska', 'swietojanska'),
    ('PrZykłaDowY tEXt', 'przykladowy-text')
])
def test_encode_text(text, expected_value):
    assert encode_text_to_url(text) == expected_value


def test_get_area(offer_markup):
    assert get_surface_for_offer(offer_markup) == 58.0


def test_get_floor(offer_markup):
    assert get_floor_for_offer(offer_markup) == 3


def test_get_price(offer_markup):
    assert get_price_for_offer(offer_markup) == 2800.0


def test_get_phone(offer_markup):
    assert get_phone_for_offer(offer_markup) == '530292133'
'''
def add(a, b):
    time.sleep(2)
    return a + b


@pytest.mark.parametrize('a,b,expected_return', [
    (1,2,3),
    (1,2,3),
    (1,2,3),
    (1,2,3),
    (1,2,3),
])
def test_add(a,b,expected_return):
    with mock.patch('tests.add') as mocked_add:
        mocked_add.return_value = 3
        assert add(a, b) == expected_return
'''