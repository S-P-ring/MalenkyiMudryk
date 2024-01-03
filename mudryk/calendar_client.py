import datetime
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build

CALENDAR_ID = os.getenv("CALENDAR_ID")


class GoogleCalendar:
    SCOPES = [os.getenv("SCOPES")]
    FILE_PATH = os.getenv("FILE_PATH")

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATH,
            scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def get_calendar_events_by_title(self, calendar_id, lesson_title):
        events = self.service.events().list(calendarId=calendar_id).execute()
        lessons = []
        for event in events['items']:
            if event['summary'] == lesson_title:
                lessons.append(event)
        return lessons

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            "id": calendar_id
        }

        return self.service.calendarList().insert(
            body=calendar_list_entry).execute()


def filter_dates(lessons_list, start_datetime):
    target_datetime = start_datetime + datetime.timedelta(days=30)
    filtered_dates = [lesson for lesson in lessons_list if
                      start_datetime <= datetime.datetime.strptime(lesson['start']['dateTime'].split('T')[0],
                                                                   '%Y-%m-%d') <= target_datetime]

    return filtered_dates


def get_lesson_days(lesson):
    obj = GoogleCalendar()
    calendar = CALENDAR_ID
    obj.add_calendar(calendar_id=calendar)
    lessons = obj.get_calendar_events_by_title(calendar_id=calendar, lesson_title=lesson)
    time_now = datetime.datetime.now()
    filtered_lessons = filter_dates(lessons, time_now)
    lesson_days = set()
    for lesson in filtered_lessons:
        date = lesson['start']['dateTime'].split('T')[0]
        lesson_days.add(date)
    lesson_days_json_response = []
    for date in lesson_days:
        date_object = datetime.datetime.strptime(date, '%Y-%m-%d')
        day_str = date_object.strftime('%A, %d %B')
        lesson_days_json_response.append({'date': date, 'day_str': day_str, 'times': []})
    for lesson in filtered_lessons:
        for date in lesson_days:
            if lesson['start']['dateTime'].split('T')[0] == date:
                time = lesson['start']['dateTime'].split('T')[1].split('+')[0]
                for date_lesson in lesson_days_json_response:
                    if date_lesson['date'] == date:
                        date_lesson['times'].append(time)
    return lesson_days_json_response
