import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import mail

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'email.html')
        self.response.out.write(template.render(path, locals()))
    def post(self):
        sender = self.request.get('sender')
        to = self.request.get('to')
        reply_to = self.request.get('reply_to')
        subject = self.request.get('subject')
        body = self.request.get('body')
        html = self.request.get('html')
        logging.info(locals())
        mailargs = locals()
        
        del mailargs['self']
        mail.send_mail(**mailargs)
        print 'Content-Type: text/plain'
        print ''
        print 'Sent.'

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
