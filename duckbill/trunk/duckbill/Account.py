import duckbill
import zebra
from duckbill import Cyclic
from duckbill import Event, Grace, Statement, Subscription
from duckbill import EncryptedCard
from pytypes import Date, DateTime
from pytypes import FixedPoint
from handy import sendmail
from strongbox import attr, link, linkset, Strongbox

class Account(Cyclic):
    """
    An account contains Subscriptions and Events
    """
    __ver__="$Id: Account.py,v 1.37 2007/05/21 03:18:03 sabren Exp $"

    ID = attr(long)
    #@TODO: unhardcode the SEI-specific brand stuff (make Brand class instead)
    brand = attr(str, default="cornerhost", okay=["cornerhost","versionhost","dcd hosting"])
    fname = attr(unicode, default="")
    lname = attr(unicode, default="")
    email = attr(str, default="")
    email2 = attr(str, default="")
    phone = attr(str, default="")
    company = attr(unicode, default="")  
    address1 = attr(unicode, default="")
    address2 = attr(unicode, default="")
    city = attr(unicode, default="")
    state = attr(unicode, default="")
    postal = attr(str, default="")
    countryCD = attr(str, default="")
    account = attr(str, default="")
    opened = attr(Date, default="today", allowNone=0)
    closed = attr(Date)
    cycLen = attr(str, okay=['month', 'year'], default='month')
    nextDue = attr(Date, default="today")
    autobill = attr(int, default=0, okay=[1,0])
    cardinfo = attr(EncryptedCard, default="")
    lastfour = attr(str)
    statementStrategy=attr(str, default="always", okay=["always","ifBalance"])
    status = attr(str, default='active',
                  okay=['active','warned','locked','closed','comped',"lifer"])
    warned = attr(Date)

    subscriptions = linkset(Subscription, "account")
    events = linkset(Event, "account")

    # @TODO: making gracePeriod a link breaks FrontEndAppTest.test_closeAccount!!
    # For some reason, Clerk just doesn't handle 1-1 relations well. :(
    # perhaps because the column in the schema dict is "ID" and that causes
    # clerk to remove it from the data it sends to storage.store() ?
    # (it was triggering an insert instead of an update, but ONLY
    # after acc.close())
    gracePeriods = linkset(Grace, "account")
    
    def get_graced(self):
        return [g for g in self.gracePeriods if not g.hasExpired()]

    def grace(self, why, untilWhen):
        self.gracePeriods << Grace(reason=why, expires=untilWhen)

    def onCatchup(self, wasDue):
        """
        Send the statement via email and record the fact that we did so.
        """
        pass
        #if wasDue:
        #    self.sendCurrentStatement()
        #    #@TODO: "and record the fact that we did so"
        

    def sendCurrentStatement(self):
        sendmail(zebra.fetch("statement", self.currentStatement()))


    def currentStatement(self):
        return Statement(self, self.whenLastStatementPosted(), duckbill.NOW)


    def whenLastStatementPosted(self):
        """
        Return date of last statement, or date opened if no statement
        ever sent.
        """
        res = self.opened
        for e in self.events:
            if (e.event == "statement") and (e.posted > res):
                res = e.posted
        return res


    def balance(self, time=None):
        """
        Return account balance at given time, or now if no time given.
        """
        cutoff = time or duckbill.NOW
        bal = FixedPoint(0.0)
        for e in self.events:
            if e.posted < cutoff:
                bal += ((e.amount or 0) * e.sign)
        return bal

    def eventsBetween(self, start, end):
        """
        Uses the python style of inclusive start, exclusive end.
        """
        res = [e for e in self.events if start <= e.posted < end]
        res.sort()
        return tuple(res)
    

    def postCharges(self):
        """
        post charges for the account's subscriptions
        """
        for sub in self.subscriptions:
            sub.catchup()
        

    def aging(self):
        credit  = 0
        charges = []

        def ischarge(x): return x > 0
        def iscredit(x): return x < 0

        for e in self.events:

            # whenever a new event is considered, we add
            # in any credit balance that might be there.
            amount = e.value + credit
            credit = 0

            # now apply this new merged value to the account:
            if ischarge(amount):
                charges.append(Event(event="charge",
                                     amount=amount,
                                     posted=e.posted))
            else:
                cash = abs(amount)
                while cash > 0:
                    if charges:
                        # apply amount to latest charge
                        owed = abs(charges[-1].amount)

                        if cash >= owed:
                            charges.pop()
                            cash -= owed
                        else:
                            charges[-1].amount -= cash
                            cash = 0
                    else:
                        credit -= cash # because credit is negative
                        cash = 0
        return charges


    def amountPastDue(self, dueDate="today"):
        """
        Given a dueDate, return the amount past due.
        This may be less than the total balance.
        """
        d = dueDate
        if not isinstance(d,Date):
            d = Date(dueDate)
        res = 0
        for e in self.aging():
            if e.posted < dueDate:
                res += e.value
        return res

    def unearnedIncome(self, cutoff):
        assert isinstance(cutoff, DateTime)
        sum = 0    
        for e in self.events:
            if e.posted <= cutoff:
                sum+=e.valueOn(cutoff)
        return -min(sum,0)

    def close(self, why):
        self.status = "closed"
        self.closed = duckbill.TODAY
        for s in self.subscriptions:
            s.close()
        self.events << Event(event="close", note=why)
