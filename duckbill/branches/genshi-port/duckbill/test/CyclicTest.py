"""
test cases for duckbill.Cyclic
"""
__ver__="$Id: CyclicTest.py,v 1.8 2005/04/22 06:44:19 sabren Exp $"

import unittest
import duckbill
from pytypes import Date
from duckbill import TODAY
from strongbox import attr

class CyclicTest(unittest.TestCase):

    def test_nextDue(self):
        cyc = duckbill.Cyclic()
        assert cyc.nextDue == None

    def test_catchup(self):
        """
        - cyclic.catchup() should call onDue()
        - This should be iterative, in case some objects
          are still due after the first cycle
        """

        duckbill.TODAY = TODAY = duckbill.Date("today")
        TOMORROW = TODAY + 1
        YESTERDAY = TODAY - 1

        class MockCyclic(duckbill.Cyclic):
            nextDue = attr(Date) # @TODO: strongbox should support inheritance!
            def __init__(self):
                super(MockCyclic, self).__init__()
                self.private.calls = {"onDue":0, "onCatchup":0}
                self.nextDue = YESTERDAY
            def calcNextDue(self):
                return self.nextDue + 1
            def onDue(self):
                self.private.calls["onDue"] += 1
            def onCatchup(self, wasDue):
                self.private.calls["onCatchup"] += 1
                self.private.wasDue = wasDue

        cyc = MockCyclic()
        cyc.catchup()

        # should be due yesterday and today.
        assert cyc.private.calls["onDue"] == 2, cyc.private.calls["onDue"]
        assert cyc.nextDue == TOMORROW
        
        # onCatchup should fire at end
        assert cyc.private.calls["onCatchup"] == 1
        assert cyc.private.wasDue

    def test_isDue(self):
        c = duckbill.Cyclic()
        assert c.nextDue is None
        self.failIf(c.isDue(), "should not be due when nextDue is None")
        
    def test_calcNextDue(self):
        """
        By default, calcNextDue should return one month after nextDue.
        """
        cyc = duckbill.Cyclic()
        cyc.nextDue = "1/1/2001"
        assert cyc.calcNextDue() == Date("2/1/2001"), \
               "expected 2/1/01, got: " + repr(cyc.calcNextDue())

        cyc.nextDue = "1/31/2001"
        assert cyc.calcNextDue() == Date("3/3/2001"), \
               "expected 3/3/01, got: " + repr(cyc.calcNextDue())


    def testCycle(self):
        cyc = duckbill.Cyclic()
        assert cyc.cycLen == 'month', "should be month by default"
        assert repr(cyc.get_cycle()) == 'MonthlyCycle()'
        cyc.cycLen = "year"
        assert cyc.cycLen == 'year', "should be year now"
        assert repr(cyc.get_cycle()) == 'YearlyCycle()'
        cyc.nextDue = ("1/1/2001")
        assert cyc.get_cycle().nextDue() == Date("1/1/2002")

        
        # just to make sure:
        sub = duckbill.Subscription()
        sub.cycLen = "year"
        assert repr(sub.cycle) == 'YearlyCycle()'


    def testLeapYear(self):
        # the evil leap year bug:
        # this was causing charges to be posted a day late
        # which meant the payment was a MONTH late.
        c = duckbill.Cyclic(cycLen="year", nextDue="3/17/2004")
        self.assertEquals(c.calcNextDue(), Date("3/17/2005"))
