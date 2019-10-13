import json
import logging
from datetime import date, timedelta, datetime
from getpass import getpass

import requests
from PyBambooHR import PyBambooHR

from config import Config
from google_calendar_client import GoogleCalendar


class CalendarSync:
    STATUS_MAP = {
        'approved': 'confirmed',
        'denied': 'tentative',
        'declined': 'tentative',
        'requested': 'tentative',
        'canceled': 'cancelled',  # This is what their API is
        'cancelled': 'cancelled'  # Just in case they fix it
    }

    def __init__(self):
        outer_config = Config()
        config = outer_config.get_config()

        try:
            token = config[Config.BAMBOO_SECTION]['token']
        except KeyError:
            # No token - try getting it from username/password
            password = getpass()
            token = CalendarSync.get_api_key(config[Config.BAMBOO_SECTION]['company'],
                                             config[Config.BAMBOO_SECTION]['user'],
                                             password)
            outer_config.save_token(token)

        self.bamboohr_client = PyBambooHR(config[Config.BAMBOO_SECTION]['company'], token)
        self.gcal_client = GoogleCalendar(config[Config.GCAL_SECTION]['calendar_id'])
        self.employee_id = config[Config.BAMBOO_SECTION]['employee_id']

    @staticmethod
    def get_api_key(company, user, password):

        logging.info('Obtaining API Key')
        payload = {'user': user, 'password': password,
                   'applicationKey': '3fdb46cdade6088a442be908141eaaada89ff6c9'}
        url = 'https://api.bamboohr.com/api/gateway.php/%s/v1/login' % company
        r = requests.post(url, data=payload, headers={'Accept': "application/json"})
        # I have no idea how long this key is valid for. Let's see when it fails
        if r.ok:
            return json.loads(r.text).get('key')
        else:
            raise Exception('Failed to get Access Token. Invalid username/password?')

    def get_time_off_requests(self):
        # Get events up to one year in the past and one year in the future
        start = (date.today() - timedelta(days=365)).isoformat()
        end = (date.today() + timedelta(days=365)).isoformat()
        return self.bamboohr_client.get_time_off_requests(start_date=start, end_date=end, employee_id=self.employee_id)

    def update_calendar(self, time_off_requests):
        print('Updating/Creating %s items' % len(time_off_requests))
        for booking in time_off_requests:
            event_id = 'emp' + booking['employeeId'] + 'id' + booking['id']
            start = booking['start']
            # Add an extra day, otherwise google will treat it as ending at the start of the last day
            end = (datetime.strptime(booking['end'], '%Y-%m-%d') + timedelta(days=1)).date().isoformat()

            status = booking['status']['status']
            notes = 'Type: ' + booking['type']['name'] + '\n'
            try:
                notes += 'Notes:\n' + '\n'.join(['  ' + str(k) + ': ' + str(v) for k, v in booking['notes'].items()])
            except AttributeError as e:
                pass
            summary = 'Time Booked off: ' + status.title()
            # Set the status to be what google calendars expents
            status = self.STATUS_MAP.get(status, 'tentative')
            logging.debug('Updating Booking: id: %s, start: %s, end: %s, status: %s, summary: %s, notes: %s',
                          event_id, start, end, status, summary, notes)
            self.gcal_client.update_event(event_id, start, end, status, summary, notes)


app = CalendarSync()
time_off = app.get_time_off_requests()
app.update_calendar(time_off)
print('Done')
