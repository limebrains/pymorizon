#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
from .utils import get_url, get_content_from_source, encode_text_to_url
import logging
log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def get_max_page(url):
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')
    last_page = markup.find_all('a', {'class': 'navigate next'})
    if not last_page:
        return 1
    num = last_page[0].previous.previous
    return int(num)


def get_category(category='nieruchomosci', city=None, street=None, transaction_type=None, url=None, **filters):
    if not url:
        city = encode_text_to_url(city or '')
        street = encode_text_to_url(street or '')
        url = get_url(category, city, street, transaction_type, **filters)
    offers = []
    max_num_of_pages = get_max_page(url)
    for i in range(1, max_num_of_pages+1):
        offers_from_page = get_offers_from_page(url + '&page=' + str(i))
        for offer_url in offers_from_page:
            offers.append(offer_url)
    return offers


def get_offers_from_page(url):
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')
    links = markup.find_all('a', {'class': 'property_link'})
    offers = []
    for link in links:
        if 'https://www.morizon.pl/oferta/' in link.get('href'):
            offers.append(link.get('href'))
    return offers
