#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import datetime as dt
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all

from morizon.utils import get_content_from_source


def get_price_for_offer(markup):
    price = markup.find_all(class_='paramIconPrice')[0].text
    price = re.findall(r'\d+,\d+|\d+', price)[0]
    return float(price)


def get_surface_for_offer(markup):
    area = markup.find_all(class_='paramIconLivingArea')[0].text
    area = re.findall(r'\d+,\d+|\d+', area)[0]
    area = area.replace(',', '.')
    return float(area)


def get_rooms_for_offer(markup):
    rooms = markup.find_all(class_='paramIconNumberOfRooms')[0].text
    rooms = re.findall(r'\d+', rooms)[0]
    return int(rooms)


def get_floor_for_offer(markup):
    soup = markup.find('table')
    floor_row = soup.find("th", text=re.compile(r'Piętro:'))
    if not floor_row:
        return None
    floor_row = floor_row.find_parent('tr').find('td').text
    floor_row = floor_row[:floor_row.index('/')]
    floor_row = re.findall(r'\d+|parter', floor_row)[0]
    if floor_row == 'parter':  floor_row = 0
    return int(floor_row)


def get_city_for_offer(markup):
    soup = markup.find_all(class_='summaryLocation')
    city = replace_all(soup[0].text, {'\n': '', 'Mieszkanie do wynajęcia Zapamiętaj ': ''})
    city = city.split(', ')
    return city[0]


def get_street_for_offer(markup):
    soup = markup.find_all(class_='summaryLocation')
    street = replace_all(soup[0].text, {'\n': '', 'Mieszkanie do wynajęcia Zapamiętaj ': ''})
    street = street.split(', ')
    return street[-1]

def get_phone_for_offer(markup):
    rooms = markup.find_all(class_='phone hidden')
    return rooms[0].text


def get_images_for_offer(markup):
    images = []
    image_list = markup.find_all(class_=re.compile(r'image\d+'))
    for link in image_list:
        src = link.img.get('data-original')
        src = src.replace('/91/64/4/', '/1280/768/16/')
        images.append(src)
    return images


def get_date_for_offer(markup):
    date = markup.find('meta', itemprop='name')
    date_added = re.findall(r'\d\d-\d\d-\d\d\d\d', date.get('content'))[0]
    date_parts = date_added.split('-')
    date_in_second = int((dt.datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])) - dt.datetime(1970, 1, 1)).total_seconds())
    return date_in_second


def get_poster_for_offer(markup):
    poster_data = markup.find(class_='ownerContact clearfix')
    poster_header = poster_data.find('strong')
    poster_name = re.findall(r'\w+ \w+|\w+', poster_header.text)[0]
    return poster_name


def get_description_for_offer(markup):
    description = markup.find(class_='description')
    return description.text


def get_gps_for_offer(markup):
    google_map = markup.find('div', class_='GoogleMap')
    if not google_map: return None
    lat = google_map.get('data-lat')
    long = google_map.get('data-long')
    gps = (lat,long)
    return gps


def get_voivodeship_for_offer(markup):
    nav = markup.find(class_='breadcrumbs').text.split('\n\n')
    return nav[3]


def get_offer_data(url):
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
