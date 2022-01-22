from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os.path
import datetime
import datefinder


SCOPES = ['https://www.googleapis.com/auth/calendar.events']

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

    # Get primary calendar  
    calendar = service.calendarList().list().execute

    # Get events from calendar and create list of start/end times
    end_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.max)
    formatted_end_day = end_day.strftime("%Y-%m-%dT%H:%M:%S" + "-05:00")
    formatted_start_day = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S" + "-05:00")
    events = service.events().list(calendarId="kewpiemayohacks@gmail.com", timeMin=formatted_start_day, timeMax=formatted_end_day).execute()
    times = []
    
    for event in events['items']:
        start_object = datetime.datetime.strptime(event['start']['dateTime'][0:19], "%Y-%m-%dT%H:%M:%S")
        end_object = datetime.datetime.strptime(event['end']['dateTime'][0:19], "%Y-%m-%dT%H:%M:%S")
        time = (start_object, end_object)
        times.append(time)

    # print(times)
    
    for i in range(1, len(times)):
        break_time = (times[i][0] - times[i-1][1]).total_seconds() / 60
        print(break_time)

# Go through list of start/end times and calculate amount of time between each event. Depending on this number, call the create_event()
# function, passing in specific arguments based on the type of break we want to create


if __name__ == '__main__':
    main()