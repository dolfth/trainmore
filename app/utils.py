"""
This module offers some basic functionality for getting, putting and
transforming the data. This module is very much written with chart.js
in mind
"""

from datetime import datetime, timedelta
from airtable import airtable
import requests
from sortedcontainers import SortedSet
from flask import current_app as app


def get_stravadata(weeks=0):
    """
    Get a maximum of 200 records from Strava. Return a list of dicts.

    Arguments:
    weeks -- the number of weeks back starting from today to get
    """
    # we need to convert the weeks into seconds from UNIX epoch for Strava
    aftersecs = 0
    if weeks > 0:
        afterdate = datetime.today() + timedelta(weeks=-weeks)
        aftersecs = afterdate.timestamp()
    payload = {'access_token': app.config['STRAVA_READ_KEY'],
               'per_page': 200, 'after': aftersecs}
    strava_read = requests.get(
        'https://www.strava.com/api/v3/athlete/activities', params=payload)
    records = strava_read.json()
    # masks the ISO8601 date so it's compatible with Airtable
    for record in records:
        record['start_date_local'] = record['start_date_local'][:10]
    return records


def get_data(weeks=0):
    """
    Joins the Airtable and Strava records
    """
    return get_stravadata(weeks) + get_airdata(weeks)


def get_airdata(weeks=0):
    """
    Get the records from the Airtable. Return a list of dicts.

    Arguments:
    weeks -- the number of weeks back starting from today to get
    """
    if weeks > 0:
        formula = ("DATETIME_DIFF(TODAY(),start_date_local,'weeks')<"
                   + str(weeks))
    else:
        formula = ''
    at_read = airtable.Airtable(app.config['AIRTABLE_BASE'],
                                app.config['AIRTABLE_READ_KEY'])
    record_generator = at_read.iterate(app.config['AIRTABLE_TABLE'],
                                       filter_by_formula=formula)
    return [x['fields'] for x in record_generator]


def put_data(data):
    """
    Puts the specified data in to the Airtable. Expects data to be in JSON
    """
    at_write = airtable.Airtable(app.config['AIRTABLE_BASE'],
                                 app.config['AIRTABLE_WRITE_KEY'])
    return at_write.create(app.config['AIRTABLE_TABLE'] , data)

def make_weeklycount(records):
    """
    Count the number of sessions for a sport per isoweek.

    Arguments:
    records -- a list of dicts containing the sessions
    """
    # convert the 'date' field to a datetime.date and add theisoweek
    for record in records:
        if 'start_date_local' in record:
            record['start_date_local'] = (
                datetime.strptime(record['start_date_local'], '%Y-%m-%d').date())
            record['week'] = (record['start_date_local'].isocalendar()[0] * 100
                              + record['start_date_local'].isocalendar()[1])
    # then, make a dataset filled with the unique weeks and sports,
    # but no counts yet.
    # This functions is possibly much nicer with a defaultdict
    unique_weeks = SortedSet(record['week'] for record in records)
    unique_sports = SortedSet(record['type'] for record in records)
    data = {'weeks': unique_weeks, 'counts': {}}
    for sport in unique_sports:
        data['counts'].update({sport: []})
    # finally for each sport and week count the occurence of that sport
    for sport in unique_sports:
        for week in unique_weeks:
            count = sum(1 if (record['week'] == week and
                              record['type'] == sport)
                        else 0 for record in records)
            data['counts'][sport].append(count)
    return data
