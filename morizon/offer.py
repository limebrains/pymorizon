#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from scrapper_helpers.utils import replace_all

from morizon.utils import get_content_from_source


def get_price_for_offer(markup):
    prices = markup.find_all(class_='paramIconPrice')
    return prices[0].text


def get_surface_for_offer(markup):
    area = markup.find_all(class_='paramIconLivingArea')
    return area[0].text


def get_rooms_for_offer(markup):
    rooms = markup.find_all(class_='paramIconNumberOfRooms')
    return rooms[0].text


def get_floor_for_offer(markup):
    soup = markup.find('table')
    floor_row = soup.find("th", text=re.compile(r'Piętro: '))
    floor_row = floor_row.find_parent('tr').find('td').text
    return floor_row


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



def get_offer_data(url):
    markup = BeautifulSoup(get_content_from_source(url).content, 'html.parser')

    return {
        'price': replace_all(get_price_for_offer(markup), {'\n': '', 'Cena': '', ' ': '', '\xa0': ' '}),
        'surface': replace_all(get_surface_for_offer(markup), {'\n': '', 'Powierzchnia': '', ' ': ''}),
        'rooms': replace_all(get_rooms_for_offer(markup), {'\n': '', 'Pokoje': ''}),
        'floor': replace_all(get_floor_for_offer(markup), {'\n': '', ' ': ''}),
        'city': get_city_for_offer(markup),
        'street': get_street_for_offer(markup),
        'phone': get_phone_for_offer(markup),
        'images': get_images_for_offer(markup)
    }
