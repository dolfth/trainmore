import os


class Config(object):
    """Parent configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-indeed'
    AIRTABLE_BASE = os.environ.get('AIRTABLE_BASE')
    AIRTABLE_TABLE = os.environ.get('AIRTABLE_TABLE', 'trainingen')
    AIRTABLE_READ_KEY = os.environ.get('AIRTABLE_READ_KEY')
    AIRTABLE_WRITE_KEY = os.environ.get('AIRTABLE_WRITE_KEY')
    STRAVA_CLIENT_ID = os.environ.get('STRAVA_CLIENT_ID')
    STRAVA_CLIENT_SECRET = os.environ.get('STRAVA_CLIENT_SECRET')
    STRAVA_READ_KEY = os.environ.get('STRAVA_READ_KEY')
    STRAVA_WRITE_KEY = os.environ.get('STRAVA_WRITE_KEY')