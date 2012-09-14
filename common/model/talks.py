from datetime import datetime
import json
from categories import category_factory
from events import events

def _get_time_from_string(time):
    lofl = [i.split(" ") for i in time.split(":")]
    l = [val for subl in lofl for val in subl]
    return formatTime(int(l[0]), int(l[1]), l[2])


def _get_talk_from_json(talk,event_code):
    category = category_factory.get(talk['category'])
    event = [event for event in events if event.code == event_code][0]
    return Talk(event,
        category,
        talk['code'],
        talk['title'],
        talk['presenters'],
        talk['emailaddress'],
        _get_time_from_string(talk['beginTime']),
        _get_time_from_string(talk['endTime']),
    )

def _parse_json_file():
    talks = []
    json_file = "common/events.json"
    json_data = json.load(open(json_file))
    for event_json in json_data:
        if "talks" in event_json:
            for talk in event_json["talks"]:
                talks.append(_get_talk_from_json(talk, event_json["code"]))
    return talks


class Talk:
    def __init__(self, event, category, code, title, presenters, emailaddress, beginTime, endTime):
        self.event = event
        self.category = category
        self.code = code
        self.title = title
        self.presenters = presenters
        self.emailaddress = emailaddress
        self.beginTime = beginTime
        self.endTime = endTime


def formatTime(hour, minute, period):
    return datetime.strptime("%d:%d %s" % (hour, minute, period), "%I:%M %p")


def formatDate(day, month, year):
    return datetime.strptim("")

talks = _parse_json_file()

class Talks:
    def get_all(self):
        return talks

    def get_talk_for_event(self, event_code, talk_code):
        return [talk for talk in talks if talk.event.code == event_code and talk.code == talk_code] or None

    def get_talk_for_event_and_category(self, event_code, category_code):
        return [talk for talk in talks if talk.event.code == event_code and talk.category.code == category_code]

