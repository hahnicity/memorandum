"""
memorandum.utils
~~~~~~~~~~~~~~~~
"""
from datetime import datetime
import requests
import ujson

from memorandum.defaults import lang, url_base
from memorandum.exceptions import HTTPStatusCodeError


def filter_zeros(data):
    """
    Removes all page view statistics with values of 0. We assume there was a
    data collection error
    """
    daily_views = {
        day: val for day, val in data["daily_views"].iteritems() if val
    }
    data.update(daily_views=daily_views)
    return data


def get_day_of_week(date_string):
    """
    Given a date formatted as "year-month-day" get the name of the day
    """
    date_split = date_string.split("-")
    datetime_obj = datetime.now().replace(
        year=int(date_split[0]), 
        month=int(date_split[1]), 
        day=int(date_split[2])
    )
    return datetime_obj.strftime("%A")


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
