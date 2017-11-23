#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
import json

import re

from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all, finder

from morizon.utils import get_content_from_source


@finder(class_='paramIconPrice', many=False)
def get_price_for_offer(item, *args, **kwargs):
    """ Parse price information

    :param item:
    :param args:
    :param kwargs:
    :return: price of offer
    :rtype: float
    """
    price = re.findall(r'\d+,\d+|\d+', item.text)[0]
    return float(price)


@finder(class_='paramIconLivingArea', many=False)
def get_surface_for_offer(item, *args, **kwargs):
    """ Parse surface area of property in offer

    :param item:
    :param args:
    :param kwargs:
    :return: surface area of property
    :rtype: float
    """
    area = item.text
    area = re.findall(r'\d+,\d+|\d+', area)[0]
    area = area.replace(',', '.')
    return float(area)


@finder(class_='paramIconNumberOfRooms', many=False)
def get_rooms_for_offer(item, *args, **kwargs):
    """ Parse number of rooms in property

    :param item:
    :param args:
    :param kwargs:
    :return: number of rooms
    :rtype: int
    """
    if not item:
        return None
    rooms = item.text
    rooms = re.findall(r'\d+', rooms)[0]
    return int(rooms)


@finder(text=re.compile(r'Piętro:'), many=False)
def get_floor_for_offer(item, *args, **kwargs):
    """ Parse floor information

    :param item:
    :param args:
    :param kwargs:
    :return: number of floor
    :rtype: int
    """
    if not item:
        return None
    floor_raw = item.find_parent('tr').find('td').text
    floor_sanitized = replace_all(floor_raw, {'\n': '', ' ': ''}).split('/')[0]
    floor = int(floor_sanitized) if floor_sanitized != 'parter' else 0
    return floor


@finder(class_='breadcrumbs', many=False)
def get_city_for_offer(item, *args, **kwargs):
    """ Parse city information

    :param item:
    :param args:
    :param kwargs:
    :return: name of city
    :rtype: str
    """
    nav = item.text.split('\n\n')
    return replace_all(nav[4], {' ': ''})


@finder(class_='summaryLocation')
def get_street_for_offer(items, *args, **kwargs):
    """ Parse street information

    :param items:
    :param args:
    :param kwargs:
    :return: name of street
    :rtype: str
    """
    soup = items[0]
    street_parts = soup.text.replace('\n\n', '').split('\n')
    return street_parts[-2]


@finder(class_='phone hidden')
def get_phone_for_offer(items, *args, **kwargs):
    """ Parse phone information

    :param items:
    :param args:
    :param kwargs:
    :return: phone number to poster
    :rtype: str
    """
    return items[0].text


@finder(class_=re.compile(r'image\d+'))
def get_images_for_offer(items, *args, **kwargs):
    """ Parse list of images of offer

    :param items:
    :param args:
    :param kwargs:
    :return: list  of images or empty list if  there is no image
    :rtype: list
    """
    return [
        link.img.get('data-original').replace('/91/64/4/', '/1280/768/16/')
        for link in items
    ]


@finder(itemprop='name', many=False)
def get_date_for_offer(item, *args, **kwargs):
    """ Parse date information

    :param item:
    :param args:
    :param kwargs:
    :return: Date of adding offer
    :rtype: int
    """
    date_added = re.findall(r'\d\d-\d\d-\d\d\d\d', item.get('content'))[0]
    date_parts = date_added.split('-')
    date_in_second = int((dt.datetime(int(date_parts[2]), int(date_parts[1]),
                                      int(date_parts[0])) - dt.datetime(1970, 1, 1)).total_seconds())
    return date_in_second


@finder(class_='ownerContact clearfix', many=False)
def get_poster_for_offer(item, *args, **kwargs):
    """ Parse poster name

    :param item:
    :param args:
    :param kwargs:
    :return: name of the poster
    :rtype: str
    """
    poster_header = item.find('strong')
    poster_name = re.findall(r'\w+ \w+|\w+', poster_header.text)[0]
    return poster_name


@finder(class_='description', many=False)
def get_description_for_offer(item, *args, **kwargs):
    """ Parse description od offer

    :param item:
    :param args:
    :param kwargs:
    :return: description
    :rtype: str
    """
    return item.text


@finder(class_='GoogleMap', many=False)
def get_gps_for_offer(item, *args, **kwargs):
    """ Parse latitude and longitude

    :param item:
    :param args:
    :param kwargs:
    :return: tuple with geographical coordinates or None if can't find
    :rtype: tuple, None
    """
    if not item:
        return None
    lat = item.get('data-lat')
    long = item.get('data-long')
    gps = (lat, long)
    return gps


@finder(class_='breadcrumbs', many=False)
def get_voivodeship_for_offer(item, *args, **kwargs):
    """ Parse voivodeship information

    :param item:
    :param args:
    :param kwargs:
    :return: name of voivodeship
    :rtype: str
    """
    nav = item.text.split('\n\n')
    return replace_all(nav[3], {' ': ''})


def get_meta_data(markup):
    data = str(markup).split('__layer.push({"property":')[1].split(',"company":')[0]
    print(data)
    data = json.loads(data)
    return data


def get_offer_data(url):
    """ Parse data from offer page url

    :param url: web page with offer
    :type url: str
    :return: Dictionary with details of an offer
    :rtype: dict
    """
    markup = BeautifulSoup(get_content_from_source(url), 'html.parser')
    meta_data = get_meta_data(markup)

    return {
        'id': meta_data.get('id'),
        'price': get_price_for_offer(markup),
        'surface': get_surface_for_offer(markup),
        'rooms': get_rooms_for_offer(markup),
        'floor': get_floor_for_offer(markup),
        'voivodeship': get_voivodeship_for_offer(markup),
        'city': get_city_for_offer(markup),
        'street': get_street_for_offer(markup),
        'phone': get_phone_for_offer(markup),
        'date_added': get_date_for_offer(markup),
        'poster_name': get_poster_for_offer(markup),
        'gps': get_gps_for_offer(markup),
        'description': get_description_for_offer(markup),
        'images': get_images_for_offer(markup),
        'url': url
    }
