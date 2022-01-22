from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os.path
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_event(service, summary, start, end):
    event = {
    'summary': summary,
    'start': {
        'dateTime': start,
        'timeZone': 'America/New_York',
    },
    'end': {
        'dateTime': end,
        'timeZone': 'America/New_York',
    },
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    service.events().insert(calendarId='kewpiemayohacks@gmail.com', body=event).execute()

def main():
    creds = None 

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('calendar', 'v3', credentials=creds)

    # Get events from calendar and create list of start/end times
    end_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.max)
    formatted_end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00")
    formatted_start_day = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S" + "-05:00")
    events = service.events().list(calendarId="kewpiemayohacks@gmail.com", timeMin=formatted_start_day, timeMax=formatted_end_day).execute()
    times = []
    times_objects = []
    
    for event in events['items']:
        print(event['summary'])
        times.append((event['start'], event['end']))
        start_object = datetime.datetime.strptime(event['start']['dateTime'][0:19], "%Y-%m-%dT%H:%M:%S")
        end_object = datetime.datetime.strptime(event['end']['dateTime'][0:19], "%Y-%m-%dT%H:%M:%S")
        time = (start_object, end_object)
        times_objects.append(time)

    times_objects.sort()
    
    for i in range(1, len(times_objects)):
        break_time = (times_objects[i][0] - times_objects[i-1][1]).total_seconds() / 60

        # Based on break_time, insert one of 5 different breaks into the calendar if possible
        if break_time >= 5 and break_time < 10:
            end = times_objects[i-1][1] + datetime.timedelta(seconds=300)
            create_event(service, 'Drink Water 💧', times_objects[i-1][1].strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"), end.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"))
        elif break_time >= 10 and break_time < 15:
            end = times_objects[i-1][1] + datetime.timedelta(seconds=600)
            create_event(service, 'Stretch 🤸‍♀️', times_objects[i-1][1].strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"), end.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"))
        elif break_time >= 15 and break_time < 20:
            end = times_objects[i-1][1] + datetime.timedelta(seconds=900)
            create_event(service, 'Meditate 🧘‍♀️', times_objects[i-1][1].strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"), end.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"))
        elif break_time >= 20 and break_time < 30:
            end = times_objects[i-1][1] + datetime.timedelta(seconds=1200)
            create_event(service, 'Go for a walk 🌿', times_objects[i-1][1].strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"), end.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"))
        elif break_time >= 30:
            end = times_objects[i-1][1] + datetime.timedelta(seconds=1800)
            create_event(service, 'Read 📚', times_objects[i-1][1].strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"), end.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00"))

if __name__ == '__main__':
    main()