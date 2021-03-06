
from storage import where
from cornerhost import User, Domain, DNSRec, EmailRule, Mailbox, Site, Database


def only(series, left, right):
    """
    Fetches one item from a series.

    Right now this only allows 'where(x)==y'
    so it could just use strings instead of where
    constructs, but I think eventually this should
    be a general purpose thing so I'll leave the
    more complex code in for now.
    """
    #assert str(cond.operation) == "=", cond.operation
    result = [x for x in series if getattr(x, left.name) == right]

    # error reporting:
    klass = series.type.__name__
    where = "where %s %s %s" % (left.name, '=', right)
    if len(result) ==  0: raise LookupError("no %s found %s" % (klass, where))
    if len(result) > 1: raise LookupError("found more than one %s %s" % (klass, where))

    return result[0]

# and here's the payoff :)
    
def safeDomain(user, domName):
    return only(user.domains,  Domain.domain, domName)

def safeEmailRule(domain, virtuser):
    return only(domain.rules, EmailRule.virtuser, virtuser)

def safeEmailRuleByID(domain, ID):
    return only(domain.rules, EmailRule.ID, int(ID))

def safeMailbox(user, mailbox):
    return only(user.boxes, Mailbox.mailbox, mailbox)

def safeSite(user, ID):
    return only(user.sites, Site.ID, int(ID))

def safeSiteByName(user, domName):
    return safeDomain(user, domName).site

def safeDNSRec(domain, ID):
    return only(domain.dnsrecs, DNSRec.ID, int(ID))

def safeDb(user, dbname):
    return only(user.dbs, Database.dbname, dbname)
