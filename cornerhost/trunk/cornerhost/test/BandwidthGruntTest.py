__ver__="$Id"
import unittest
import cornerhost.config
from clerks import MockClerk, Schema
from storage import MockStorage
from cornerhost import BandwidthGrunt, User, Usage, Plan
from duckbill import Account
from pytypes import Date
from decimal import Decimal
from handy import GIGA
from strongbox import *


TODAY = Date("today")

class MockUser(Strongbox):
    bandused = attr(long)
    bandquota = attr(long)
    def trafficUsed(self, period):
        return self.bandused

class BandwidthGruntTest(unittest.TestCase):
    
    def setUp(self):
        self.clerk = MockClerk(Schema(cornerhost.config.DBMAP))
        self.rate = Decimal("1.23") # dollars per gig... :)
        self.bwg = BandwidthGrunt(self.clerk, self.rate)
        
    def test_findDueAccounts(self):
        
        # one due today, one tomorrow, one today but versionhost
        a = self.clerk.store(Account(account='a', nextDue=TODAY))
        b = self.clerk.store(Account(account='b', nextDue=TODAY+1))
        c = self.clerk.store(Account(account='c', nextDue=TODAY,
                                     brand="versionhost"))
        
        due = self.bwg.findDueAccounts()
        assert due == [a]
        

    def test_findUsersForAccount(self):

        a = Account()
        u1 = self.clerk.store(User(account=a))
        u2 = self.clerk.store(User(account=Account()))
        u3 = self.clerk.store(User(account=a))

        users = self.bwg.findUsersForAccount(a)
        assert users == [u1, u3]


    def test_monthlyTraffic(self):

        arbdate = Date("2/29/2004")
        startdate = Date("1/29/2004")

        user = User()

        # this one is out of range:
        user.usage << Usage(whichday=startdate-1, traffic= 1 * GIGA)

        # this one is cool:
        user.usage << Usage(whichday=startdate, traffic=  2 * GIGA)

        # these are good:
        user.usage << Usage(whichday=arbdate-3, traffic=  4 * GIGA)
        user.usage << Usage(whichday=arbdate-2, traffic=  8 * GIGA)
        user.usage << Usage(whichday=arbdate-1, traffic= 16 * GIGA)

        # this one is in the "future", since it
        # won't be recorded until "tonight":
        user.usage << Usage(whichday=arbdate, traffic= 32 * GIGA)
        
        self.assertEquals(self.bwg.monthlyTraffic(user, arbdate),
                          (2 + 4 + 8 + 16) * GIGA)


    def test_calcOverage(self):
        user = MockUser(bandused=3*GIGA, bandquota=1*GIGA)
        assert self.bwg.calcOverage(user, TODAY) == 2*GIGA

        user = MockUser(bandused=2*GIGA, bandquota=5*GIGA)
        assert self.bwg.calcOverage(user, TODAY) == 0


    def test_calcCharge(self):
        
        # overage:
        user = MockUser(bandused=3*GIGA, bandquota=1*GIGA)
        self.assertEquals(self.rate * 2, self.bwg.calcCharge(user, TODAY))

        # partial charge:
        user = MockUser(bandused=3*GIGA, bandquota=2.5*GIGA)
        self.assertEquals(self.rate / 2, self.bwg.calcCharge(user, TODAY))

        # no overage:
        user = MockUser(bandused=3*GIGA, bandquota=50*GIGA)
        self.assertEquals(0, self.bwg.calcCharge(user, TODAY))


    def test_chargeAccounts(self):

        plan = Plan(bandquota=GIGA)
        u1 = User(plan=plan, account=Account(), username="ftempy")
        u1.usage << Usage(whichday=TODAY-1, traffic=1*GIGA)
        u1.usage << Usage(whichday=TODAY-2, traffic=1*GIGA)
        u1 = self.clerk.store(u1)
        self.bwg.chargeAccounts(TODAY)
        self.assertEquals(self.rate, u1.account.balance())
        assert u1.account.events[0].note == "bandwidth overage [ftempy]"

        u2 = self.clerk.store(User(plan=plan, account=Account()))
        self.bwg.chargeAccounts(TODAY)
        assert u2.account.balance()==0
        assert len(u2.account.events) == 0 # don't want $0.00 charges


if __name__=="__main__":
    unittest.main()
