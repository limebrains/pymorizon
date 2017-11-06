#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
import requests
from . import BASE_URL
from scrapper_helpers.utils import replace_all

log = logging.getLogger(__file__)
POLISH_CHARACTERS_MAPPING = {"ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s", "ż": "z", "ź": "z"}

def get_city(location):
    location = replace_all(location.lower(), POLISH_CHARACTERS_MAPPING)
    city = location.split()
    for element in city:
        if element == 'ul.':
            city.remove(city.index(element))
    return city

def get_content_from_sorce(url):
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