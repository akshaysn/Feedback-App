from controller import HomePageHandler, ViewPageHandler, SummaryPageHandler, AjaxHandler, AppHomePageHandler
import webapp2


app = webapp2.WSGIApplication([(r'/(\w+)', HomePageHandler),
						   (r'/(\w+)/summary', SummaryPageHandler),
						   (r'/(\w+)/(\w+)', ViewPageHandler),
						   (r'/(\w+)/ajax/(\w+)', AjaxHandler),
						   (r'/', AppHomePageHandler),
						   ], debug=True)