#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import requests
from urllib.parse import quote, urlparse, unquote

from bs4 import BeautifulSoup

from . import BASE_URL
from scrapper_helpers.utils import replace_all, get_random_user_agent, caching, key_md5

log = logging.getLogger(__file__)
POLISH_CHARACTERS_MAPPING = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z"}
POSSIBLE_CATEGORIES = ['mieszkania', 'domy', 'komercyjne', 'dzialki', 'garaze', 'pokoje']
POSSIBLE_TRANSACTIONS = ['do-wynajecia']

def get_max_page(url):
    """ Reads total page number on Morizon search page

    :param url:  web page url
    :type url: str
    :return: number on sub web pages for search
    :rtype: int
    """
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')
    last_page = markup.find_all('a', {'class': 'navigate next'})
    if not last_page:
        return 1
    num = last_page[0].previous.previous
    return int(num)


def encode_text_to_url(text):
    """ Change text to lower cases, gets rid of polish characters replacing them with simplified version, replaces spaces with dashes

    :param text: raw text
    :type text: str
    :return: encoded text which can be used in url
    :rtpe: str
    """
    replace_dict = POLISH_CHARACTERS_MAPPING
    replace_dict.update({' ': '-'})
    return replace_all(text.lower(), replace_dict)


class URL:
    def __init__(self, category='nieruchomosci', city=None, street=None, transaction_type=None, filters=None):
        self.filters = filters or {}
        self.transaction_type = transaction_type
        self.street = street
        self.city = city
        self.category = category
        self.page = 1

    def get_url(self):
        """ Create Morizon search web page with given parameters

        :param category: type of property of interest (mieszkania/domy/garaże/działki)
        :param city: city
        :param street:  street
        :param transaction_type: type of transaction(sprzedaż/wynajem)
        :param filters: Dictionary with additional filters.
        :type category: str, None
        :type city: str, None
        :type street: str, None
        :type transaction_type: str, None
        :type filters: dict
        :return: url to web page
        :rtype: srt
        """
        url = BASE_URL
        if self.transaction_type:
            url += '/' + self.transaction_type
        url += '/' + encode_text_to_url(self.category)
        if self.city:
            url += '/' + encode_text_to_url(self.city)
        if self.street:
            url += '/' + encode_text_to_url(self.street)
        url += '/?page={0}&'.format(self.page)
        if self.filters and len(self.filters) > 0:
            for i, param in enumerate(self.filters):
                url += "ps{0}={1}&".format(quote(param), self.filters[param])
        return url

    @classmethod
    def from_string(cls, url):
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')[1:-1]
        transaction, category, city, street = None, 'nieruchomosci', None, None
        for i, path_part in enumerate(path_parts):
            if path_part == 'nieruchomosci':
                pass
            elif path_part in POSSIBLE_TRANSACTIONS:
                transaction = path_part
            elif path_part in POSSIBLE_CATEGORIES:
                category = path_part
            elif not city:
                city = path_part
            else:
                street = path_part

        filters = {}
        query_params = parsed_url.query.split('ps')[1:]
        for i, query_param in enumerate(query_params):
            query_param, value = replace_all(query_param, {'%5B': '[', '%5D': ']', '&': ''}).split('=')
            filters[query_param] = value

        return cls(category, city, street, transaction, filters)

    def next_page(self):
        self.page += 1
        return self

    def max_num_of_pages(self):
        return get_max_page(self.get_url())


@caching(key_func=key_md5)
def get_content_from_source(url):
    """ Connects with given url

    If environmental variable DEBUG is True it will cache response for url in /var/temp directory

    :param url: Website url
    :type url: str
    :return: Response for requested url
    """
    response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        log.warning('Request for {0} failed. Error: {1}'.format(url, e))
        return None
    return response


def finder(many=True, *finder_args, **finder_kwargs):
    def decorator(fun):
        def wrapper(markup, *args, **kwargs):
            if many:
                items = markup.find_all(*finder_args, **finder_kwargs)
            else:
                items = markup.find(*finder_args, **finder_kwargs)
            kwargs.update({'markup': markup})
            return fun(items, *args, **kwargs)
        return wrapper
    return decorator
