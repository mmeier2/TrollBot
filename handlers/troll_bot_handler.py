import webapp2

class TrollBotHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('We up and running')