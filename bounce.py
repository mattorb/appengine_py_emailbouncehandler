#!/usr/bin/env python
# encoding: utf-8

class NotABounceMessage(Exception):
    pass

class BounceParser():
    def __init__(self, subject, message):
        self.subject=subject
        self.message=message
        
    def isBounce(self):
        return self.subject == 'Delivery Status Notification (Delay)' or self.subject == 'Delivery Status Notification (Failure)'

    def isPermanent(self):
        self._checkBounce()
        return self.subject == 'Delivery Status Notification (Failure)'

    def isTemporary(self):
        self._checkBounce()
        return self.subject == 'Delivery Status Notification (Delay)'
    
    def replyTo(self):
        self._checkBounce()
        (statusinfo, originalmessage) = self.message.split('----- Original message -----')
        
        for line in originalmessage.split('\n'):
            if line.startswith('Reply-To: '):
                return line.split('Reply-To: ')[1]
        
    def originalMessageContent(self):
        self._checkBounce()
        (statusinfo, originalmessage) = self.message.split('----- Original message -----')
        
        return originalmessage.strip().split('\n\n',1)[1]
        
    def failureAddress(self):
        self._checkBounce()
        beforeDetail = self.message.split('Technical details')[0]

        for line in beforeDetail.split('\n'):
            if '@' in line:     #todo replace with a regex?
                return line.strip()
    
    def error(self):
        self._checkBounce()
        (statusinfo, originalmessage) = self.message.split('----- Original message -----')
        
        if 'Technical details of temporary failure:' in statusinfo:
            return statusinfo.split('Technical details of temporary failure:')[1].strip()
        else:
            return statusinfo.split('Technical details of permanent failure:')[1].strip()
        
    def _checkBounce(self):
        if not self.isBounce():
            raise NotABounceMessage
