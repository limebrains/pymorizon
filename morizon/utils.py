#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
import requests
from . import BASE_URL
from scrapper_helpers.utils import replace_all, get_random_user_agent

log = logging.getLogger(__file__)
POLISH_CHARACTERS_MAPPING = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z"}


def encode_text_to_url(text):
    replace_dict = POLISH_CHARACTERS_MAPPING
    replace_dict.update({' ': '-'})
    return replace_all(text.lower(), replace_dict)


def get_url(category='nieruchomosci', city=None, street=None, transaction_type=None, **filters):
    url = BASE_URL
    if transaction_type:
        url += '/' + transaction_type
    url += '/' + category
    if city:
        url += '/' + encode_text_to_url(city)
    if street:
        url += '/' + encode_text_to_url(street)
    if len(filters) > 0:
        i = 0
        for param in filters:
            if i == 0:
                url += '/?ps' + param + '=' + str(filters[param])
            else:
                url += '&ps' + param + '=' + str(filters[param])
            i += 1
    return url


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
