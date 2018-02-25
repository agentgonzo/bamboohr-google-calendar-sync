import argparse
import logging
import os

import httplib2
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'google-calendar-client-secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


class GoogleCalendar:

    def __init__(self, calendar_id):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.config/bamboohr')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'google-calendar.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(credential_path + CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        http = credentials.authorize(httplib2.Http())
        self.events = discovery.build('calendar', 'v3', http=http).events()
        self.calendar_id = calendar_id

    def update_event(self, id, start, end, status, summary, description):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        event = {
            'id': id,
            'start': {'date': start},
            'end': {'date': end},
            'summary': summary,
            'description': description,
            'status': status
        }
        try:
            self.events.patch(eventId=id, calendarId=self.calendar_id, body=event).execute()
        except HttpError as e:
            logging.info('Could not patch event, trying to create instead')
            self.events.insert(calendarId=self.calendar_id, body=event).execute()


if __name__ == '__main__':
    GoogleCalendar('k7u1kb46aja6i0ue67etm0u2fk@group.calendar.google.com') \
        .update_event('1234567', '2018-02-26', '2018-02-26', 'confirmed', 'Summary', 'Desc')
