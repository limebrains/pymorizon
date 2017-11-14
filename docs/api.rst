Introduction
============
pymorizon supplies two methods that can be used to scrape data from Morizon website

.. _categories:

======================
Scraping category data
======================
This method scrapes available offer urls from Morizon search results with parameters
.. autofunction:: morizon.category.get_category

The function above can be used like this:

::

    filters = {'[number_of_rooms_from]: 2'}
    offers_url = morizon.category.get_category('mieszkania', 'Gdańsk', 'Grunwaldzka', 'do-wynajecia', None, filters)

The code above will put a list of urls containing all apartments found in the given category into the offers_url variable

===================
Scraping offer data
===================
This method scrapes details of offer
.. autofunction:: morizon.offer.get_offer_data

The function above can be used like this:

::

    details = morizon.offer.get_offer_data(url)

the code above will create dictionary with details of offer from given url
