#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
from urllib.parse import quote
from .utils import URL, get_content_from_source, encode_text_to_url
import logging

log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)


def get_category(category='nieruchomosci', city=None, street=None, transaction_type=None, url=None, filters=None):
    """ Parses available offer urls from given category from every page

    :param category: type of property of interest (mieszkania/domy/garaże/działki)
    :param city: city
    :param street:  street
    :param transaction_type: type of transaction(sprzedaż/wynajem)
    :param url: User defined url for Morizon page with offers. It overrides other parameters
    :param filters: Dictionary with additional filters.
    :type category: str, None
    :type city: str, None
    :type street: str, None
    :type transaction_type: str, None
    :type url: str, None
    :type filters: dict
    :return: List of urls of all offers for given parameters
    :rtype: list
    """
    if not url:
        city = encode_text_to_url(city or '')
        street = encode_text_to_url(street or '')
        if filters:
            filters['page'] = 1
        url = URL(category, city, street, transaction_type, filters=filters)
    offers = []
    max_num_of_pages = url.max_num_of_pages()
    for i in range(1, max_num_of_pages + 1):
        offers_from_page = get_offers_from_page(url.get_url())
        for offer_url in offers_from_page:
            offers.append(offer_url)
        url.next_page()
    return offers


def get_offers_from_page(url):
    """ Parses available offer urls from given category from given page

    :param url: Defined url for Morizon page with offers
    :type url: str
    :return: List of urls of offers from page
    :rtype: list
    """
    print(url)
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')
    links = markup.find_all('a', {'class': 'property_link'})
    offers = []
    for link in links:
        if 'https://www.morizon.pl/oferta/' in link.get('href'):
            offers.append(link.get('href'))
    return offers
