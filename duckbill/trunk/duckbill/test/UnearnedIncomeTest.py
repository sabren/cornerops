import unittest
from decimal import Decimal
from duckbill import Event, Account
from pytypes import Date

def unearned(events, cutoff=Date("today")):
    a = Account()
    for e in events:
        a.events << e
    return a.unearnedIncome(cutoff)

def chg(amt, posted="today", maturity="today"):
    return Event(event="charge", amount=amt, posted=posted, maturity=maturity)

def pay(amt, posted="today"):
    return Event(event="payment", amount=amt, posted=posted)

class UnearnedIncomeTest(unittest.TestCase):   

    def testSimpleReport(self):
        self.assertEquals(unearned([]),       0)
        self.assertEquals(unearned([chg(5)]), 0)
        self.assertEquals(unearned([pay(5)]), 5)
        self.assertEquals(unearned([chg(5), pay(5)]), 0)

    def testReportWithTime(self):
        today = Date("today")
        yesterday = today-1
        tomorrow = today+1
        nextday = today+2        
        events = [chg(5, yesterday),
                  pay(10,today),
                  chg(3, tomorrow, tomorrow),
                  chg(5, nextday, nextday)]
        self.assertEquals(unearned(events, yesterday), 0)
        self.assertEquals(unearned(events, today), 5)
        self.assertEquals(unearned(events, tomorrow), 2)
        self.assertEquals(unearned(events, nextday), 0)

        c,p = chg(100, today, today+30), pay(100, today)
        for x in range(-50,0):
            day = today + x
            goal = 0
            actual = unearned([c,p], day)
            assert actual==goal, "%s vs %s on day %s" % (actual, goal, x)
        for x in range(0,50):
            day = today + x
            goal = c.amount - c.valueOn(day)
            actual = unearned([c,p], day)
            assert actual==goal, "%s vs %s on day %s" % (actual, goal, x)
            

    def testVestingPreconditions(self):
        "make sure Event requires valid dates in order"
        e = Event(event="charge", amount="100")
        e.maturity=None; e.posted = "1/1/2002"
        self.assertRaises(AssertionError, e.percentVested, Date("1/1/2002"))

        e.posted = None; e.maturity = "1/1/2002"
        self.assertRaises(AssertionError, e.percentVested, Date("1/1/2002"))

        e.posted = "1/2/2002"; e.maturity = "1/1/2002"
        self.assertRaises(AssertionError, e.percentVested, Date("1/1/2002"))

    def testVesting(self):
        "ensure charges are slowly 'earned' over time"
        e = Event(event="charge", amount="50",
                  posted="1/1/2000", maturity="11/1/2000")
        assert e.percentVested(e.posted) == 0
        assert e.percentVested(e.posted-1) == 0
        assert e.percentVested(e.maturity) == 100
        assert e.percentVested(e.maturity+1) == 100

        #@TODO: paramaterize number of decimal places ?

        # In a single month, we're fully vested at the end of the month.
        # With a yearly charge, the vesting happens slowly over time.
        d = Decimal
        self.assertEquals(e.percentVested(Date("2/1/2000")), d('10.16'))
        self.assertEquals(e.percentVested(Date("5/1/2000")), d('39.67'))
        self.assertEquals(e.percentVested(Date("7/1/2000")), d('59.67'))
        self.assertEquals(e.percentVested(Date("10/1/2000")), d('89.84'))
        self.assertEquals(e.percentVested(Date("10/31/2000")), d('99.67'))
        self.assertEquals(e.percentVested(Date("11/1/2000")), d('100.00'))
        self.assertEquals(e.percentVested(Date("12/1/2000")), d('100.00'))

        # valueOn should multiply by amount
        e.amount = 200
        self.assertEquals(e.valueOn(Date("2/1/2000")), d('20.32'))


if __name__=="__main__":
    unittest.main()
    
