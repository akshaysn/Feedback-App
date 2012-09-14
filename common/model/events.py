# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from categories import Category, category_factory
import json

def _get_event_details_from_json(event_dict):
    categories = [category_factory.get(category) for category in event_dict["categories"]]
    return EventDetail(event_dict["code"],
        event_dict["title"],
        event_dict["header"],
        event_dict["isArchived"],
        categories)

def _parse_json_file():
    events = []
    json_file = "common/events.json"
    json_data = json.load(open(json_file))
    for event_json in json_data:
        event = _get_event_details_from_json(event_json)
        events.append(event)
    return events

class EventDetail:
    def __init__(self, code, title, header, isArchived, categories):

        self.code = code
        self.title = title
        self.header = header
        self.isArchived = isArchived
        self.categories = categories


class Event:
    XCONF = EventDetail('xconf', 'XConf', 'XConf Feedback', True,
                        [Category.BLITZ, Category.RAPID, Category.CLASSIC, Category.XCONF])
    BACONF = EventDetail('baconf', 'BAConf', 'BAConf Feedback', True, [Category.TALK, Category.CONF])

events = _parse_json_file()

class Events:
    def get_all(self):
        return events

    def get_all_codes(self):
        return [e.code for e in events]

    def get_categories_for_event(self, event_code):
        return [e for e in events if e.code == event_code][0].categories




