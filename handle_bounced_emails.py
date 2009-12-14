import logging
import email # pyflakes:ignore
import bounce
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app

class BounceHandler(InboundMailHandler):
    def receive(self, mail_message):
        (type, payload) = mail_message.bodies(content_type='text/plain').next()
        text = payload.decode()

        bp = bounce.BounceParser(mail_message.subject, text)

        logging.info("Bounced? %s" % bp.isBounce())
        
        if bp.isBounce():
            logging.info("Originally to: %s" % bp.failureAddress())
            logging.info("Perm? %s Temp? %s" % (bp.isPermanent(), bp.isTemporary()))
            logging.info("Reply-to: %s" % bp.replyTo())
            logging.info("Error: %s" % bp.error())
            logging.info("Text: %s" % bp.originalMessageContent())
            
            # do something here like notify the user, or flag it in your tracking system/datastore
        else:
            pass # do your normal e-mail handling for anything sent to this address here...

application = webapp.WSGIApplication([BounceHandler.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()


