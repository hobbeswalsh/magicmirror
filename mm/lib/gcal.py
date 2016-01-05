from __future__ import print_function
import os
import datetime as dt

import httplib2
from apiclient import discovery

import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_events(future_days=1, max_results=10):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = dt.datetime.utcnow()
    end = now + dt.timedelta(days=future_days)

    now_str = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    end_str = end.isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now_str, timeMax=end_str, maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        start = event["start"].get("dateTime")
        if start is not None:
            start_dt = dt.datetime.strptime(start[:19], '%Y-%m-%dT%H:%M:%S')
            all_day = False
        else:
            start = event["start"].get("date")
            start_dt = dt.datetime.strptime(start, '%Y-%m-%d')
            all_day = True
        event["all_day"] = all_day
        event["start_dt"] = start_dt

    return {"events": events}


if __name__ == '__main__':
    print(get_events())
