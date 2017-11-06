#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
from .utils import get_content_from_sorce
import logging
log = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)

def get_category(category='nieruchomosci', location=None, transaction_type=None, url=None, **filters):
    """ Parses available offer urls from given category from every page

    :param url: User defined url for OLX page with offers. It overrides category parameters and applies search filters.
    :param category: Main category
    :param location: Region of search
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
    :type location: str, None
    :type filters: dict
    :return: List of all offers for given parameters
    :rtype: list
    """
    assert False
    return 'dd'


def get_offers_from_page(page, category='nieruchomosci', location=None, transaction_type=None, url=None, **filters):
    """ Parses offers for one specific page of given category with filters.

        :param page: Page number
        :param url: User defined url for OLX page with offers. It overrides category parameters and applies search filters.
        :param category: Category of property
        :param location: Region of search
        :param transaction_type: Type of transaction # buy/rent
        :param filters: See :meth category.get_category for reference
        :type page: int
        :type url: str, None
        :type category: str, None
        :type location: str, None
        :type filters: dict
        :return: List of all offers for given page and parameters
        :rtype: list
        """
    if not url:
        sorce = 'https://www.morizon.pl/'
        if transaction_type != '':
            sorce += transaction_type + "/"
        sorce += category + "/"
        if location != '':
            city = get_city(location)
            for element in city:
                sorce += element + "/"
        for i in range(len(filters)):
            if i == 0:
                sorce += "?ps"
            else:
                sorce += "&ps"
            sorce += filters.keys()[i] + "=" + filters.values()[i]
        if page > 1:
            sorce += "&page=" + str(page)
    else:
        sorce = url

    response = get_content_from_sorce(sorce)
    offers = parse_available_offers(response.content)
    return offers
