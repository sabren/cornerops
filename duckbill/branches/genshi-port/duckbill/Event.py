from pytypes import DateTime, Date
from pytypes import FixedPoint
from pytypes import toDateTime
from strongbox import *
from strongbox import Strongbox
import duckbill

# @TODO: it might be interesting to make Clerk accept a
# factory so I can break event into lots of little
# classes...

class Event(Strongbox):
    """
    Event (line items)
    """
    __ver__="$Id: Event.py,v 1.29 2006/07/02 06:08:09 sabren Exp $"

    ID = attr(long)
    account = link(lambda : duckbill.Account)
    event = attr(str, default='payment',
                 okay=['open','charge','payment','credit',
                       'statement','note','close','debit',"void"])
    posted = attr(DateTime, default="now")
    maturity = attr(Date, default=None)
    amount = attr(FixedPoint, default=0)
    note = attr(str)
    adminnote = attr(str)
    source = attr(str, default='n/a',
                  okay=['bofa','paypal','check','other','n/a'])
    refnum = attr(str)

    _signs = {
        'charge': 1,
        'debit': 1,
        'payment': -1,
        'credit': -1,
        'statement': 0,
        'void':0,
        'note': 0,
        'close':0,}
        
    def get_sign(self):
        return self._signs[self.event]

    def __cmp__(self, other):
        return cmp(self.posted, other.posted) or cmp(self.value, other.value)
    
    #@TODO: combine these two?
    def get_value(self):
        return (self.amount or 0) * (self.sign or 0)
    def valueOn(self, date):
        if self.event=="charge":
            return (self.percentVested(date)* self.amount)/100.0
        else:
            return self.value
        

    def percentVested(self, when):
        """
        returns percent vested
        """
        assert self.event == "charge", "vesting only applies to  charges"
        assert self.posted is not None, "vesting requires .posted"
        assert self.maturity is not None, "vesting requires .maturity"
        assert self.posted.toDate() <= self.maturity, "can't mature before posting!"
        if not isinstance(when, DateTime):
            raise TypeError, "when must be DateTime, not %s" % type(when)

        # that checked out, so now:
        if when >= self.maturity:
            return 100
        elif when <= self.posted:
            return 0
        else:
            # return percentage of time until maturity
            abPosted = self.posted.toMx().absdate
            abWhen = when.toMx().absdate
            abMature = self.maturity.toMx().absdate

            totalDays = abMature - abPosted
            pastDays = abWhen - abPosted
            return 100.0 * pastDays / totalDays
