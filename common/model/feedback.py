from google.appengine.ext import db
from datetime import time, datetime, timedelta
from dbproperty import JsonProperty

import ast 
import inspect


class EventFeedback(db.Model):
	provider = db.StringProperty()
	event = db.StringProperty()
	talk = db.StringProperty()
	content = JsonProperty()
	createdOn = db.DateTimeProperty(auto_now_add=True)

def format_IST(datevalue):
	datevalue = datevalue + timedelta(hours=5, minutes=30)
	return datevalue.strftime("%d %b %Y, %I:%M %p")


def get_attr_value(feedback, attr_name):
	if hasattr(feedback, attr_name):
		return getattr(feedback, attr_name)

	content = ast.literal_eval(feedback.content)

	if attr_name in content:
		return content[attr_name]

	return None

def get_talk_feedbacks(talk_code='CONF'):
	return EventFeedback.gql("WHERE talk = :1 ORDER BY createdOn DESC", talk_code).fetch(1000)

def get_all_feedbacks():
	return EventFeedback.gql("WHERE talk != :1", 'DUMMY').fetch(1000)

def get_average(feedbacks, rating):
	return 0 if len(feedbacks) == 0 else  sum( [ int(get_attr_value(feedback,rating)) for feedback in feedbacks]) / len(feedbacks)

def get_count(feedbacks, name, value):
	return 0 if len(feedbacks) == 0 else  len ([ feedback for feedback in feedbacks if get_attr_value(feedback, name) == str(value) ])

def get_distinct_count(feedbacks, name):
	return 0 if len(feedbacks) == 0 else  len ( set ( [ get_attr_value(feedback, name) for feedback in feedbacks ] ) )


def save_feedback(feedbackContent, event_code, talk_code='FEED', provider='Anonymous'):
	feedback = EventFeedback()
	feedback.content = feedbackContent
	feedback.event = event_code
	feedback.provider = provider
	feedback.talk = talk_code
	feedback.put()
	return feedback
