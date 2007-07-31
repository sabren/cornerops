"""
test cases for Account
"""
__ver__="$Id: AccountTest.py,v 1.13 2006/07/02 06:08:09 sabren Exp $"

import unittest
import duckbill
import duckbill.spec
from duckbill import Account, Event, Subscription
from pytypes import Date

class AccountTest(unittest.TestCase):

    def test_whenLastStatementPosted(self):
        """
        This should find the statement with the latest 'posted' time.
        """
        acc = duckbill.spec.fakeAccount()
        acc.opened = Date("1/1/2001")
        assert acc.whenLastStatementPosted() == Date("1/1/2001")
        assert len(acc.events) == 0
        acc.events << duckbill.newEvent("statement", posted="2/1/2001")
        acc.events << duckbill.newEvent("statement", posted="5/1/2001")
        acc.events << duckbill.newEvent("statement", posted="3/1/2001")
        acc.events << duckbill.newEvent("statement", posted="1/1/2001")
        assert acc.whenLastStatementPosted() == Date("5/1/2001")
        

    def test_currentStatement(self):
        """
        This should return a Statement with all data since last Statement.
        """
        pass # it's only one line... The magic's in Statement.__init__

    def test_balance(self):
        acc = duckbill.spec.fakeAccount()
        nEv = duckbill.newEvent

        assert acc.balance() == 0
        acc.events << nEv("charge", posted="1/1/2001", amount=5)
        assert acc.balance() == 5
        assert acc.balance(Date("12/31/2000")) == 0
        assert acc.balance(Date("1/1/2001")) == 0
        assert acc.balance(Date("1/2/2001")) == 5
        
    def test_eventsBetween(self):
        acc = duckbill.spec.fakeAccount()
        then = Date("1/1/2001")
        now = Date("5/1/2001") # not really :)

        # start with nothing.
        assert len(acc.eventsBetween(then, now)) == 0

        # include the front date:        
        acc.events << duckbill.newEvent("payment", posted="1/1/2001")
        assert len(acc.eventsBetween(then, now)) == 1, "start"

        # exclude the end date:
        acc.events << duckbill.newEvent("note", posted="5/1/2001")
        assert len(acc.eventsBetween(then, now)) == 1, "end"

        # include the middle:
        acc.events << duckbill.newEvent("charge", posted="2/1/2001")
        acc.events << duckbill.newEvent("credit", posted="4/1/2001")
        l = len(acc.eventsBetween(then, now))
        assert l == 3, \
                "middle should have 3 events, actually has %d" % l


    def oldAccount(self):
        acc = Account()
        acc.events << Event(event="charge", amount=10, posted="1/1/2002")
        acc.events << Event(event="charge", amount=10, posted="2/1/2002")
        acc.events << Event(event="credit", amount=5,  posted="2/2/2002")

        acc.events << Event(event="charge", amount=10, posted="3/1/2002")
        acc.events << Event(event="charge", amount=10, posted="4/1/2002")
        acc.events << Event(event="credit", amount=20, posted="4/2/2002")
        acc.events << Event(event="charge", amount=10, posted="5/1/2002")

        assert acc.balance() == 25
        return acc

    def test_aging(self):
        acc = self.oldAccount()
        
        goal = (Event(event="charge", amount=10, posted="1/1/2002"),
                Event(event="charge", amount=5,  posted="2/1/2002"),
                Event(event="charge", amount=10, posted="5/1/2002"))
        actual = acc.aging()

        for a, g in zip(actual, goal):
            assert (a.value == g.value) and (a.posted==g.posted), \
                   "aging isn't working correctly!"

    def test_amountPastDue(self):
        acc = self.oldAccount()
        assert acc.amountPastDue(Date("today")) == 25
        assert acc.amountPastDue("today") == 25
        assert acc.amountPastDue("4/1/2002") == 15
        assert acc.amountPastDue("1/15/2002") == 10
        assert acc.amountPastDue("1/1/2002") == 0
        
        
    def test_BadPastDue(self):
        """
        This was a bug I noticed in the receivables page.
        """
        acc = Account()

        acc.events << Event(event="charge", amount=20, posted="09/15/2002")
        acc.events << Event(event="charge", amount= 4, posted="09/16/2002")
        acc.events << Event(event="payment", amount=20,posted="09/19/2002")
        
        assert acc.balance() == 4, acc.balance()
        self.assertEquals(acc.amountPastDue("09/20/2002"), 4)
        aging = acc.aging()
        assert len(aging)==1
        assert aging[0].value == 4


    def test_cardinfo(self):
        acc = Account()        
        assert str(acc.cardinfo) == ""
        acc.cardinfo.owner="fred tempy"
        self.assertRaises(Exception, str, acc.cardinfo)
        acc.cardinfo.number = "1234"
        acc.cardinfo.expire = "today"
        import duckbill.config
        duckbill.config.GNUPG_RECIPIENT="encrypted.card.test@sabren.com"
        assert str(acc.cardinfo).count("BEGIN PGP")


    def test_close(self):
        acc = Account()
        sub = Subscription()
        old = Subscription(status="closed", closed="1/1/2004")
        acc.subscriptions << old
        acc.subscriptions << sub
        assert acc.closed is None
        assert sub.closed is None
        acc.close("closed for nonpayment")
        assert acc.status == "closed"
        assert sub.status == "closed"
        assert acc.closed == duckbill.TODAY
        assert sub.closed == duckbill.TODAY
        assert old.closed == "1/1/2004"

        evt = acc.events[-1]
        assert evt.event == "close"
        assert evt.note == "closed for nonpayment"
        
if __name__=="__main__":
    unittest.main()

