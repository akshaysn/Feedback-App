import webapp2
import jinja2
import os
import cgi
import logging
import json
import uuid
import datetime
import ast

import utils
from google.appengine.api import channel, memcache
from model.feedback import *
from model.events import Events
from model.talks import Talks


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
jinja_environment.filters['avg'] = get_average
jinja_environment.filters['agg'] = get_count
jinja_environment.filters['dst'] = get_distinct_count
jinja_environment.filters['val'] = get_attr_value
jinja_environment.filters['format_IST'] = format_IST

html_path = 'html/'
talk_cache = {}

class AppHomePageHandler(webapp2.RequestHandler):
    def get(self):
        logging.info('Requested Url:' + self.request.url)
        template_values = {"events": Events().get_all()}
        template = jinja_environment.get_template(html_path + 'app_home.html')
        self.response.out.write(template.render(template_values))


class HomePageHandler(webapp2.RequestHandler):
    def get(self, event_code):
        logging.info('Requested Url:' + self.request.url)

        event_code = event_code.lower()
        event = utils.find(lambda e: event_code == e.code, Events().get_all())

        if event is None:
            self.response.write('Resource Not Found')
            self.set_status(404)
            return

        template_values = {'header': event.header, 'categories': Events().get_categories_for_event(event_code),
                           'action': event_code}

        logging.info('Html Path: ' + html_path + 'home.html')

        template = jinja_environment.get_template(html_path + 'home.html')
        self.response.out.write(template.render(template_values))

    def post(self, event_code):
        logging.info('Post Action:' + event_code)

        event_code = event_code.lower()
        event = utils.find(lambda e: event_code == e.code, Events().get_all())

        talk_code = self.request.get('talk_code') or 'CONF'
        talk = Talks().get_talk_for_event(event_code, talk_code)

        if ((event is None) or (talk is None)):
            self.response.write('Resource Not Found')
            self.response.set_status(404)
            return

        talk = talk[0]

        template_values = {}
        comment = template_values['comment'] = cgi.escape(self.request.get('comment'))
        ratingA = template_values['ratingA'] = cgi.escape(self.request.get('ratingA'))
        ratingB = template_values['ratingB'] = cgi.escape(self.request.get('ratingB'))
        ratingC = template_values['ratingC'] = cgi.escape(self.request.get('ratingC'))
        provider = template_values['provider'] = cgi.escape(self.request.get('provider')) or 'Anonymous'
        template_values['talk_code'] = talk_code
        template_values['header'] = event.header
        template_values['title'] = talk.title
        template_values['presenters'] = talk.presenters

        logging.info('Talk Code: %s Posted Content: %s ' % (talk_code, comment))

        feedbackContent = {'comment': comment,
                           'ratingA': ratingA,
                           'ratingB': ratingB,
                           'ratingC': ratingC}

        save_feedback(json.dumps(feedbackContent), event_code, talk_code, provider)

        template = jinja_environment.get_template(html_path + 'message.html')
        self.response.out.write(template.render(template_values))


class ViewPageHandler(webapp2.RequestHandler):
    def get(self, event_code, talk_code):
        logging.info('Event Code: %s Talk Code: %s ' % (event_code, talk_code))
        talk_code = talk_code.upper()
        event_code = event_code.lower()

        event = utils.find(lambda e: event_code == e.code, Events().get_all())
        talk = Talks().get_talk_for_event(event_code, talk_code)

        if((talk is None) or (event is None)):
            self.response.write('Resource Not Found')
            self.response.set_status(404)
            return

        talk = talk[0]

        logging.info('Talk Details: ' + talk.code)

        feedbacks = get_talk_feedbacks(talk_code)

        template_values = {}
        template_values['feedbacks'] = feedbacks
        template_values['talk'] = talk
        template_values['header'] = event.header
        template_values['feedbacksCount'] = len(feedbacks)
        template_values['averageRating'] = 0 if len(feedbacks) == 0 else  sum(
            [int(ast.literal_eval(feedback.content)['ratingC']) for feedback in feedbacks]) / len(feedbacks)

        template = jinja_environment.get_template(html_path + 'view.html')
        self.response.out.write(template.render(template_values))


class SummaryPageHandler(webapp2.RequestHandler):
    def get(self, event_code):
        event_code = event_code.lower()
        event = utils.find(lambda e: event_code == e.code, Events().get_all())
        if(event is None):
            self.response.write('Resource Not Found')
            self.set_status(404)
            return

        template_values = {}

        feedbacks = get_all_feedbacks()
        template_values['feedbacks'] = feedbacks
        template_values['feedbacksCount'] = len(feedbacks)

        template = jinja_environment.get_template(html_path + 'summary.html')
        self.response.out.write(template.render(template_values))


class AjaxHandler(webapp2.RequestHandler):
    def get(self, eventId, categoryId):
        logging.info('Event: %s Category: %s ' % (eventId, categoryId))

        key = eventId + '#' + categoryId

        if( key in talk_cache ):
            self.response.out.write(talk_cache[key])
            return

        logging.info('Cache Miss for %s' % key)

        talks_for_category = Talks().get_talk_for_event_and_category(eventId, categoryId)
        records = []
        for talk in talks_for_category:
            talktitle = talk.title
            if talk.category.show_time:
                talktitle = "%s (%s - %s)" % (
                talk.title, talk.beginTime.strftime("%I:%M %p"), talk.endTime.strftime("%I:%M %p"))

            records.append(
                {"code": "" + talk.code + "", "title": "" + talktitle + "", "presenters": "" + talk.presenters + "",
                 "category": "" + talk.category.displayName + ""})

        talk_cache[categoryId] = json.dumps(records)
        self.response.out.write(talk_cache[categoryId])
