from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
import datefinder
import informationExtracter
from argparse import ArgumentParser

import datetime

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'credentials.json'
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
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# def main():
#     """Shows basic usage of the Google Calendar API.

#     Creates a Google Calendar API service object and outputs a list of the next
#     10 events on the user's calendar.
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('calendar', 'v3', http=http)

#     # Refer to the Python quickstart on how to setup the environment:
#     # https://developers.google.com/google-apps/calendar/quickstart/python
#     # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
#     # stored credentials.

#     event = {
#       'summary': 'Exam',
#       'location': '',
#       'description': 'Exam I: Monday September 19th, 2016',
#       'start': {
#         'dateTime': '2016-09-19T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'end': {
#         'dateTime': '2016-09-19T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#       ],
#       'attendees': [
#         {'email': 'lpage@example.com'},
#         {'email': 'sbrin@example.com'},
#       ],
#       'reminders': {
#         'useDefault': False,
#         'overrides': [
#           {'method': 'email', 'minutes': 24 * 60},
#           {'method': 'popup', 'minutes': 10},
#         ],
#       },
#     }

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print ('Event created: %s' % (event.get('htmlLink')))


def main(summary, description, date):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.
    year = date[0].year
    month = date[0].month
    day = date[0].day

    event = {
      'summary': f'{summary}',
      'location': '',
      'description': f'{description}',
      'start': {
        'dateTime': f'{year}-{month}-{day}T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': f'{year}-{month}-{day}T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

#if __name__ == '__main__':
argparser = ArgumentParser()
argparser.add_argument('--filename', help="Path to the file.")
args = argparser.parse_args()
file = args.filename
#print("***", file)

print("Loading...")
data = informationExtracter.run(file)
for eventDate in data:
    summary = data[eventDate][0]
    description = data[eventDate][1]
    date = list(datefinder.find_dates(eventDate.text))
    if len(date) == 0:
        print('Not a vaild date')
        break
    main(summary, description, date)
        #main()


# from __future__ import print_function
# import httplib2
# import os

# from apiclient import discovery
# import oauth2client
# from oauth2client import client
# from oauth2client import tools
# from oauth2client import file

# import datetime
# from informationExtracter import *

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/calendar-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/calendar'
# CLIENT_SECRET_FILE = 'credentials.json'
# APPLICATION_NAME = 'Google Calendar API Python Quickstart'


# def get_credentials():
#     """Gets valid user credentials from storage.

#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.

#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'calendar-python-quickstart.json')

#     store = oauth2client.file.Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)
#         print('Storing credentials to ' + credential_path)
#     return credentials


# def getEvents(file = None):
#     bio = "./Syllabuses/BIOL 1107 Fall 2016 Syllabus.pdf"
#     mys = SyllabusParser(bio)
#     mys.parse()
#     events = mys.addEventsPg(1)

#     info = [] #[(date, )]
#     for date in events:
#         print(date)
#         eventType = events[date][0]
#         eventSentence = events[date][1]
#         filename = bio
#         info.append((date, eventType, eventSentence, filename))
#     return info

# # def parseDate(date):
# #     values = {'january' : 01,
# #         'february' : 02,
# #         'march' : 03,
# #         'april' : 04,
# #         'may' : 05,
# #         'june' : 06,
# #         'july' : 07,
# #         'august' : 08,
# #         'september' : 09, 
# #         'october' : 10,
# #         'november' : 11,
# #         'december' : 12 }
    
#     # if 
#     # date = date.split()
#     # year = date.split()[-1]
#     # month = 

# # def main():
# #     """Shows basic usage of the Google Calendar API.

# #     Creates a Google Calendar API service object and outputs a list of the next
# #     10 events on the user's calendar.
# #     """
# #     credentials = get_credentials()
# #     http = credentials.authorize(httplib2.Http())
# #     service = discovery.build('calendar', 'v3', http=http)

# #     # Refer to the Python quickstart on how to setup the environment:
# #     # https://developers.google.com/google-apps/calendar/quickstart/python
# #     # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# #     # stored credentials.

# #     #date, eventType, eventSentence, filename = getEvents()
# #     # y,m,d = parseDate(date)

# #     # d = '0' + str(int(d))
# #     # m = '0' + str(int(m))

# #     event = {
# #       'summary': 'Exam',
# #       'location': '',
# #       'description': 'Exam I: Monday September 19th, 2016',
# #       'start': {
# #         'dateTime': '2016-09-16T09:00:00-07:00',
# #         'timeZone': 'America/Los_Angeles',
# #       },
# #       'end': {
# #         'dateTime': '2016-09-16T17:00:00-07:00',
# #         'timeZone': 'America/Los_Angeles',
# #       },
# #       'recurrence': [
# #         'RRULE:FREQ=DAILY;COUNT=2'
# #       ],
# #       'attendees': [
# #         {'email': ''},
# #         {'email': ''},
# #       ],
# #       'reminders': {
# #         'useDefault': False,
# #         'overrides': [
# #           {'method': 'email', 'minutes': 24 * 60},
# #           {'method': 'popup', 'minutes': 10},
# #         ],
# #       },
# #     }

# #     event = service.events().insert(calendarId='primary', body=event).execute()
# #     print('Event created: %s' % (event.get('htmlLink')))

# def main():
#     """Shows basic usage of the Google Calendar API.

#     Creates a Google Calendar API service object and outputs a list of the next
#     10 events on the user's calendar.
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('calendar', 'v3', http=http)

#     # Refer to the Python quickstart on how to setup the environment:
#     # https://developers.google.com/google-apps/calendar/quickstart/python
#     # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
#     # stored credentials.

#     event = {
#       'summary': 'Exam',
#       'location': '',
#       'description': 'Lorem',
#       'start': {
#         'dateTime': '2019-05-28T09:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'end': {
#         'dateTime': '2019-05-28T17:00:00-07:00',
#         'timeZone': 'America/Los_Angeles',
#       },
#       'recurrence': [
#         'RRULE:FREQ=DAILY;COUNT=2'
#       ],
#       'attendees': [
#         {'email': ''},
#         {'email': ''},
#       ],
#       'reminders': {
#         'useDefault': False,
#         'overrides': [
#           {'method': 'email', 'minutes': 24 * 60},
#           {'method': 'popup', 'minutes': 10},
#         ],
#       },
#     }

#     event = service.events().insert(calendarId='primary', body=event).execute()
#     print ('Event created: %s' % (event.get('htmlLink')))

# if __name__ == '__main__':
#     main()