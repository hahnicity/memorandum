"""
memorandum.finder
~~~~~~~~~~~~~~~~~

Finds page view statistics for a given wikipedia page
"""
from datetime import datetime

from memorandum.constants import get_workweek
from memorandum.utils import (
    filter_zeros, 
    get_day_of_week,
    get_monthly_data
)


def count_page_views_for_month(month, wiki_page, year=None):
    """
    Get the aggregate number of page views for a wiki page in a given month
    """
    year = year or datetime.now().year
    formatted_date = "{}{}".format(year, month)
    aggregate_views = 0
    data = get_monthly_data(formatted_date, wiki_page)
    for views in data["daily_views"].itervalues():
        aggregate_views += views
    return aggregate_views


def get_page_views_for_year(wiki_page, year=None):
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


def group_by_week(data):
    """
    Group daily data by week (SMTWTFS)
    """
    week_separated_data = []
    week = []
    workweek = get_workweek()
    sorted_data = sorted(
        data["daily_views"].items(), key=lambda (day, val): day
    )
    initial_day = get_day_of_week(sorted_data[0][0])
    previous_day_of_workweek = workweek[initial_day]
    week.append(sorted_data[0])

    for data_point in sorted_data[1:]:
        day_of_workweek = workweek[get_day_of_week(data_point[0])]
        if day_of_workweek > previous_day_of_workweek:
            week.append(data_point)
        else:
            week_separated_data.append(week)
            week = []
            week.append(data_point)
        previous_day_of_workweek = day_of_workweek

    return week_separated_data
