import unittest
from bounce import BounceParser, NotABounceMessage

class TestBounce(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def testBounceParsePermanent(self):
        (subject, message)=('Delivery Status Notification (Failure)',
"""
Delivery to the following recipient failed permanently:

    failed@address.com

Technical details of permanent failure:
DNS Error: Domain name not found

----- Original message -----

MIME-Version: 1.0
Reply-To: Joe Schmoe <joe@schmoe.com>
X-Google-Appengine-App-Id: emailbouncehandler
Received: by 10.101.4.27 with SMTP id g27mr5767010ani.5.1260806729231; Mon, 14
       Dec 2009 08:05:29 -0800 (PST)
Message-ID: <005045015fd739eeb1047ab27158@google.com>
Date: Mon, 14 Dec 2009 16:05:29 +0000
Subject: Joe Schmoe invited you to Coffee at Starbucks Coffee. Cast your
       vote quick!
From: Joe Schmoe <adminaccount@yourapp.com>
To: inviteduser@otherdomain.com
Content-Type: multipart/alternative; boundary=005045015fd739ee97047ab27155

Message Content
goes here1
"""
        )
        bp = BounceParser(subject=subject, message=message)
        
        self.assertTrue(bp.isBounce())
        self.assertTrue(bp.isPermanent())
        self.assertFalse(bp.isTemporary())
        self.assertEquals('Joe Schmoe <joe@schmoe.com>', bp.replyTo())
        self.assertEquals('failed@address.com', bp.failureAddress())
        self.assertEquals('DNS Error: Domain name not found', bp.error())
        self.assertEquals('Message Content\ngoes here1', bp.originalMessageContent())

    def testBounceParseTemporary(self):
        (subject, message)=('Delivery Status Notification (Delay)',
"""
This is an automatically generated Delivery Status Notification

THIS IS A WARNING MESSAGE ONLY.

YOU DO NOT NEED TO RESEND YOUR MESSAGE.

Delivery to the following recipient has been delayed:

    delayed@address.com

Technical details of temporary failure:
The recipient server did not accept our requests to connect. Learn more at http://mail.google.com/support/bin/answer.py?answer=7720
[address.com (1): Connection refused]

----- Original message -----

MIME-Version: 1.0
Reply-To: Bob Schmob <bob@schmob.com>
X-Google-Appengine-App-Id: emailbouncehandler
Received: by 10.101.4.27 with SMTP id g27mr5767010ani.5.1260806729231; Mon, 14
       Dec 2009 08:05:29 -0800 (PST)
Message-ID: <005045015fd739eeb1047ab27158@google.com>
Date: Mon, 14 Dec 2009 16:05:29 +0000
Subject: Joe Schmoe invited you to Coffee at Starbucks Coffee. Cast your
       vote quick!
From: Joe Schmoe <adminaccount@yourapp.com>
To: inviteduser@otherdomain.com
Content-Type: multipart/alternative; boundary=005045015fd739ee97047ab27155

Message Content
goes here2
"""
)
        bp = BounceParser(subject=subject, message=message)

        self.assertTrue(bp.isBounce())
        self.assertFalse(bp.isPermanent())
        self.assertTrue(bp.isTemporary())
        self.assertEquals('Bob Schmob <bob@schmob.com>', bp.replyTo())
        self.assertEquals('delayed@address.com', bp.failureAddress())
        self.assertEquals('The recipient server did not accept our requests to connect. Learn more at http://mail.google.com/support/bin/answer.py?answer=7720\n[address.com (1): Connection refused]', bp.error())
        self.assertEquals('Message Content\ngoes here2', bp.originalMessageContent())

    def testBounceParseNotABounceMessage(self):
        (subject, message)=('Hey who are you?', 'This is just a normal e-mail message addressed to the app.....')
        bp = BounceParser(subject=subject, message=message)

        self.assertFalse(bp.isBounce())
        self.assertRaises(NotABounceMessage, bp.isPermanent)
        self.assertRaises(NotABounceMessage, bp.isTemporary)
        self.assertRaises(NotABounceMessage, bp.replyTo)
        self.assertRaises(NotABounceMessage, bp.failureAddress)
        self.assertRaises(NotABounceMessage, bp.error)
        self.assertRaises(NotABounceMessage, bp.originalMessageContent)

if __name__ == '__main__':
    unittest.main()