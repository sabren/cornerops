# fake data for testing
from cornerhost.schema import User, Server, Domain, EmailRule, Site, Plan
from cornerhost.grunts import UserClerk
from clerks import MockClerk, Schema
from cornerhost.config import DBMAP


def makePerson(username, domain):
    user = User(username="fred",
                plan=Plan(name="script"),
                diskusing=3000000,
                server=Server(name="mockium"))
    dom = user.domains << Domain(domain=domain)
    dom.site = user.sites << Site(domain=dom)
    dom.rules << EmailRule(virtuser='spam', mailto='error:nouser')
    dom.rules << EmailRule(virtuser=username, mailto="~")
    return user

def makeFred(clerk):
    return clerk.store(makePerson("fred", "fred.com"))

def makeWanda(clerk):
    return clerk.store(makePerson("wanda", "wanda.com"))    

def fredClerk():
    clerk = MockClerk(Schema(DBMAP))
    return UserClerk(makeFred(clerk), clerk)
