#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all

from morizon.utils import get_content_from_source


def get_price_for_offer(markup):
    prices = markup.find_all(class_='paramIconPrice')
    return prices[0].text


def get_surface_for_offer(markup):
    prices = markup.find_all(class_='paramIconLivingArea')
    return prices[0].text


def get_rooms_for_offer(markup):
    prices = markup.find_all(class_='paramIconNumberOfRooms')
    return prices[0].text


def get_offer_data(url):
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')

    return {
        'price': replace_all(get_price_for_offer(markup), {'\n': '', 'Cena': '', ' ': '', '\xa0': ' '}),
        'surface': replace_all(get_surface_for_offer(markup), {'\n': '', 'Powierzchnia': '', ' ': ''})
    }
