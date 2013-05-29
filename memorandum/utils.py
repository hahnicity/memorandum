"""
memorandum.utils
~~~~~~~~~~~~~~~~
"""
from datetime import datetime


def convert_wiki_date_to_datetime(date_string, **kwargs):
    """
    Converts a date formatted as "year-month-day" to a datetime object
    """
    date_split = date_string.split("-")
    now = datetime.now()
    return now.replace(
        year=int(date_split[0]), 
        month=int(date_split[1]), 
        day=int(date_split[2]),
        hour=kwargs.get("hour", now.hour),
        minute=kwargs.get("minute", now.minute),
        second=kwargs.get("second", now.second)
    )


def filter_for_values(data):
    """
    Given a set of data this will take all the daily view statistics, strip
    the dates and then return a large list of only page views
    """
    return data["daily_views"].values()


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
    datetime_obj = convert_wiki_date_to_datetime(date_string)
    return datetime_obj.strftime("%A")
