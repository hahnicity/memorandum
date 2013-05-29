"""
memorandum.finder
~~~~~~~~~~~~~~~~~

Finds page view statistics for a given wikipedia page
"""
from datetime import datetime

import requests
import ujson

from memorandum.defaults import url_base, lang
from memorandum.exceptions import HTTPStatusCodeError
from memorandum.utils import filter_zeros


def get_yearly_data(wiki_page, year=None):
    """
    Get dictionary of page views for a wiki page in a given year
    """
    yearly_data = {}
    year = year or datetime.now().year
    for i in xrange(1, 13):
        month = "{0:02}".format(i)
        formatted_date = "{}{}".format(year, month)

        # Initialize data for January otherwise update daily views
        data = get_monthly_data(formatted_date, wiki_page)
        if i == 1:
            yearly_data = data
        else:
            yearly_data["daily_views"].update(data["daily_views"])
    
    yearly_data = filter_zeros(yearly_data)
    return yearly_data


def get_monthly_data(date_string, wiki_page):
    """
    Get a json blob of the monthly page view data for a given wiki page

    date_string should be given as a combination of a nonspace separated
    year and month
    eg: 201206

    wiki_page should be given as the desired wikipedia page eg: Apple_Inc.
    which was taken from the suffix of http://en.wikipedia.org/wiki/Apple_inc
    """
    response = requests.get("{}/json/{}/{}/{}".format(
        url_base, lang, date_string, wiki_page)
    )
    if response.status_code != 200:
        raise HTTPStatusCodeError(response)
    else:
        return ujson.loads(response.text)
