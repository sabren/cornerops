import duckbill
from decimal import Decimal
from duckbill import Event
from duckbill import Cyclic
from pytypes import Date
from strongbox import *

class Subscription(Cyclic):
    """
    A subscription billed to an account.
    """
    __ver__="$Id: Subscription.py,v 1.36 2006/07/02 06:08:09 sabren Exp $"

    ID = attr(long)
    account = link(lambda : duckbill.Account)
    service = attr(str)
    username = attr(str)
    note  = attr(str)
    rate = attr(Decimal)
    opened = attr(Date, default="today")
    closed = attr(Date)
    cycLen = attr(str, okay=['month', 'year'], default='month')
    nextDue = attr(Date, default="today")
    status = attr(str, okay=['active','closed'], default='active')

    def _fetch(self, **where):
        super(Subscription, self)._fetch(**where)
        if self._data['closed']:
            if self._data['closed'].find('0000') > -1:
                self._data['closed'] = None

    #@TODO: move me into Cycle! (maybe?)
    def calcCharge(self):
        return self.rate

    def calcNote(self):
        """
        Note that appears on charges. Extracted so it's easy to override.
        """
        return "1-%s %s [%s]" % (self.cycLen, self.service, self.username)


    def onDue(self):
        """
        Post the recurring charge to the subscription's account.
        """
        self.account.events << Event(
            event="charge",
            posted=self.nextDue,
            maturity=self.calcNextDue(),
            note=self.calcNote(),
            amount=self.calcCharge())

    def close(self):
        if self.status != "closed":
            self.closed = duckbill.TODAY
            self.status = "closed"
