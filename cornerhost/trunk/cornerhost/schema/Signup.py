__ver__="$Id: Signup.py,v 1.3 2007/04/18 07:08:57 sabren Exp $"
from strongbox import *
from pytypes import DateTime, EmailAddress
from duckbill import Account, Subscription

# note: this file is symlinked in various places!!

class Signup(Strongbox):
    ID = attr(long)
    TS = attr(DateTime, default="now")
    fname = attr(str)
    lname = attr(str)
    email = attr(EmailAddress)
    company = attr(str)
    phone = attr(str)
    addr1 = attr(unicode)
    addr2 = attr(unicode)
    city = attr(unicode)
    state = attr(str)
    postal = attr(str)
    country = attr(str, default="USA")
    username = attr(str) # user (web) or repository (cvs)
    plan = attr(str, default="personal")
    spacex50 = attr(int, default=0) # extra 50mb allowances
    cycLen = attr(str, okay=["month","year"], default="month")
    
    service = attr(str, default="web")
    ipaddress = attr(str)
    description = attr(str)
    comments = attr(str)
    status = attr(str, okay=['new','rejected','filled','cancelled'], default='new')
    #paymeth = attr(str, okay=["credit","paypal","check"])


    def get_fullname(self):
        return self.fname + " " + self.lname


    def get_brand(self):
        return "cornerhost"



    def get_rates(self):
        return {
            "shell": 20,
            "script": 10,
            "basic": 5,
            }
        
    def calcRate(self):
        assert self.plan in self.rates, "unknown plan: %s" % self.plan
        if self.cycLen == "year":
            return self.rates[self.plan] * 10
        else:
            return self.rates[self.plan]


    def _makeSubscriptions(self):
        """
        returns a list of subscriptions to add to
        the ducbkill account.
        @TODO: mysql, space, pop3, etc...
        """
        return [Subscription(
                   username = self.username,
                   service = self.plan,
                   rate = self.calcRate(),
                   cycLen = self.cycLen,
                   nextDue = "today" )]


    def toDuckbill(self):
        """
        Returns a duckbill Account with the appropriate
        Subscriptions and Events. 
        """
        a = Account(
                fname = self.fname,
                lname = self.lname,
                email = self.email,
                company = self.company,
                phone = self.phone,
                address1 = self.addr1,
                address2 = self.addr2,
                city = self.city,
                state = self.state,
                postal = self.postal,
                countryCD = self.country,
                account = self.username,
                brand = self.brand, )

        for s in self._makeSubscriptions():
            # hmmm... is it good that I need both of these?
            # probably i need a bidirectional link object
            s.account = a
            a.subscriptions << s
            s.catchup()
        return a 
