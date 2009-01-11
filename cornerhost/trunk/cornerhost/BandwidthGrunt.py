
from cornerhost import User
from duckbill import Account, Event
from pytypes import PythonicRange
from handy import daysInMonthPriorTo, GIGA

class BandwidthGrunt(object):
    """
    I am responsible for charging users
    and/or shutting down their accounts
    when they exceed their bandwidth quotas.
    """

    def __init__(self, clerk, ratePerGig):
        self.clerk = clerk
        self.ratePerGig = ratePerGig
        
    def findDueAccounts(self):
        return [
            a for a
            in self.clerk.match(Account, brand="cornerhost")
            if (a.status != "closed") and (a.isDue())
        ]

    def findUsersForAccount(self, ac):
        """
        This method sucks, but I don't want duckbill
        to know about cornerhost, so there's no Account.users
        """
        return self.clerk.match(User, accountID=ac.ID)


    def monthlyTraffic(self, user, date):
        return user.trafficUsed(
            PythonicRange(date - daysInMonthPriorTo(date),
                          date))


    def calcOverage(self, user, date):
        return max(0, (self.monthlyTraffic(user, date) - user.bandquota))

    def calcCharge(self, user, date):
        return self.calcOverage(user,date)* self.ratePerGig / GIGA


    def chargeAccounts(self, date):
        for a in self.findDueAccounts():
            dirty = 0
            for u in self.findUsersForAccount(a):
                charge = self.calcCharge(u, date)
                if charge:
                    dirty = True
                    a.events << Event(event="charge",
                                      amount=charge,
                                      posted=date,
                                      note=("bandwidth overage [%s]"
                                            % u.username))
            if dirty:
                self.clerk.store(a)
