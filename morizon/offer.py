#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import datetime as dt
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all, caching, key_md5
from morizon.utils import get_content_from_source


def get_price_for_offer(markup):
    """ Parse price information

    :param markup: Source of offer web page
    :type markup: str str
    :return: price of offer
    :rtype: float
    """
    price = markup.find_all(class_='paramIconPrice')[0].text
    price = re.findall(r'\d+,\d+|\d+', price)[0]
    return float(price)


def get_surface_for_offer(markup):
    """ Parse surface area of property in offer

    :param markup: Source of offer web page
    :type markup: str
    :return: surface area of property
    :rtype: float
    """
    area = markup.find_all(class_='paramIconLivingArea')[0].text
    area = re.findall(r'\d+,\d+|\d+', area)[0]
    area = area.replace(',', '.')
    return float(area)


def get_rooms_for_offer(markup):
    """ Parse number of rooms in property

    :param markup: Source of offer web page
    :type markup: str
    :return: number of rooms
    :rtype: int
    """
    try:
        rooms = markup.find_all(class_='paramIconNumberOfRooms')[0].text
    except IndexError:
        return None
    rooms = re.findall(r'\d+', rooms)[0]
    return int(rooms)


def get_floor_for_offer(markup):
    """ Parse floor information

    :param markup: Source of offer web page
    :type markup: str
    :return: number of floor
    :rtype: int
    """
    soup = markup.find('table')
    floor_row = soup.find("th", text=re.compile(r'Piętro:'))
    if not floor_row:
        return None
    floor_raw = floor_row.find_parent('tr').find('td').text
    floor_sanitized = replace_all(floor_raw, {'\n': '', ' ': ''}).split('/')[0]
    floor = int(floor_sanitized) if floor_sanitized != 'parter' else 0
    return floor


def get_city_for_offer(markup):
    """ Parse city information

    :param markup: Source of offer web page
    :type markup: str
    :return: name of city
    :rtype: str
    """
    nav = markup.find(class_='breadcrumbs').text.split('\n\n')
    return replace_all(nav[4], {' ': ''})


def get_street_for_offer(markup):
    """ Parse street information

    :param markup: Source of offer web page
    :type markup: str
    :return: name of street
    :rtype: str
    """
    soup = markup.find_all(class_='summaryLocation')[0]
    street_parts = soup.text.replace('\n\n', '').split('\n')
    print(street_parts[-2])
    return street_parts[-2]

'''
@finder(class_='phone hidden')
def get_phone_for_offer(items):
    """ Parse phone information

    :param markup: Source of offer web page
    :type markup: str
    :return: phone number to poster
    :rtype: str
    """
    return items[0].text


@finder(class_=re.compile(r'image\d+'))
def get_images_for_offer(items):
    """ Parse list of images of offer

    :param markup: Source of offer web page
    :type markup: str
    :return: list  of images or empty list if  there is no image
    :rtype: list
    """
    return [
        link.img.get('data-original').replace('/91/64/4/', '/1280/768/16/')
        for link in items
    ]
'''

def get_phone_for_offer(markup):
    """ Parse phone information

    :param markup: Source of offer web page
    :type markup: str
    :return: phone number to poster
    :rtype: str
    """
    rooms = markup.find_all(class_='phone hidden')
    return rooms[0].text


def get_images_for_offer(markup):
    """ Parse list of images of offer

    :param markup: Source of offer web page
    :type markup: str
    :return: list  of images or empty list if  there is no image
    :rtype: list
    """
    images = []
    image_list = markup.find_all(class_=re.compile(r'image\d+'))
    for link in image_list:
        src = link.img.get('data-original')
        src = src.replace('/91/64/4/', '/1280/768/16/')
        images.append(src)
    return images


def get_date_for_offer(markup):
    """ Parse date information

    :param markup: Source of offer web page
    :type markup: str
    :return: Date of adding offer
    :rtype: int
    """
    date = markup.find('meta', itemprop='name')
    date_added = re.findall(r'\d\d-\d\d-\d\d\d\d', date.get('content'))[0]
    date_parts = date_added.split('-')
    date_in_second = int((dt.datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])) - dt.datetime(1970, 1, 1)).total_seconds())
    return date_in_second


def get_poster_for_offer(markup):
    """ Parse poster name

    :param markup: Source of offer web page
    :type markup: str
    :return: name of the poster
    :rtype: str
    """
    poster_data = markup.find(class_='ownerContact clearfix')
    poster_header = poster_data.find('strong')
    poster_name = re.findall(r'\w+ \w+|\w+', poster_header.text)[0]
    return poster_name


def get_description_for_offer(markup):
    """ Parse description od offer

    :param markup: Source of offer web page
    :type markup: str
    :return: description
    :rtype: str
    """
    description = markup.find(class_='description')
    return description.text


def get_gps_for_offer(markup):
    """ Parse latitude and longitude

    :param markup: Source of offer web page
    :type markup: str
    :return: tuple with geographical coordinates or None if can't find
    :rtype: tuple, None
    """
    google_map = markup.find('div', class_='GoogleMap')
    if not google_map: return None
    lat = google_map.get('data-lat')
    long = google_map.get('data-long')
    gps = (lat,long)
    return gps


def get_voivodeship_for_offer(markup):
    """ Parse voivodeship information

    :param markup: Source of offer web page
    :type markup: str
    :return: name of voivodeship
    :rtype: str
    """
    nav = markup.find(class_='breadcrumbs').text.split('\n\n')
    return replace_all(nav[3], {' ': ''})


def get_offer_data(url):
    """ Parse data from offer page url

    :param url: web page with offer
    :type url: str
    :return: Dictionary with details of an offer
    :rtype: dict
    """
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')

    return {
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
