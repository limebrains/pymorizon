#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
from .utils import get_city, get_url, get_content_from_sorce
import logging
log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)

def get_max_page(url):
    content = get_content_from_sorce(url)



def get_category(category='nieruchomosci', city=None, streat=None, transaction_type=None, url=None, **filters):
    """ Parses available offer urls from given category from every page

    :param url: User defined url for morizon page with offers. It overrides category parameters and applies search filters.
    :param category: Main category
    :param city: Region of search
    :param streat: Region of search
    :param filters: Dictionary with additional filters. Following example dictionary contains every possible filter
    with examples of it's values.

    :Example:

    input_dict = {
        "[filter_float_price:from]": 2000, # minimal price
        "[filter_float_price:to]": 3000, # maximal price
        "[filter_enum_floor_select][0]": 3, # desired floor, enum: from -1 to 11 (10 and more) and 17 (attic)
        "[filter_enum_furniture][0]": True, # furnished or unfurnished offer
        "[filter_enum_builttype][0]": "blok", # valid build types:
        #                                             blok, kamienica, szeregowiec, apartamentowiec, wolnostojacy, loft
        "[filter_float_m:from]": 25, # minimal surface
        "[filter_float_m:to]": 50, # maximal surface
        "[filter_enum_rooms][0]": 2 # desired number of rooms, enum: from 1 to 4 (4 and more)
    }

    :type url: str, None
    :type category: str, None
    :type city: str, None
    :type streat: str, None
    :type filters: dict
    :return: List of all offers for given parameters
    :rtype: list
    """
    if not url:
        city = get_city(city)
        url = get_url(category, city, streat, transaction_type, **filters)
    
    '''
    offers = []
    no_of_pages = get_max_page(url)
    for i in range(1, no_of_pages+1):
        offer = get_offers_from_page(i, url=url)
    '''
    return url


def get_offers_from_page(page, category='nieruchomosci', city=None, streat=None, transaction_type=None, url=None, **filters):
    """ Parses offers for one specific page of given category with filters.

        :param page: Page number
        :param url: User defined url for morizon page with offers. It overrides category parameters and applies search filters.
        :param category: Category of property
        :param city: Region of search
        :param streat: Region of search
        :param transaction_type: Type of transaction # buy/rent
        :param filters: See :meth category.get_category for reference
        :type page: int
        :type url: str, None
        :type category: str, None
        :type city: str, None
        :type streat: str, None
        :type filters: dict
        :return: List of all offers for given page and parameters
        :rtype: list

    if not url:

    else:
        sorce = url

    response = get_content_from_sorce(sorce)
    offers = parse_available_offers(response.content)
    return offers
 """