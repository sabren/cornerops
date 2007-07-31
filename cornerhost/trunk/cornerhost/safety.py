
from storage import where
from cornerhost import User, Domain, DNSRec, EmailRule, Mailbox, Site, Database


def only(series, cond):
    """
    Fetches one item from a series.

    Right now this only allows 'where(x)==y'
    so it could just use strings instead of where
    constructs, but I think eventually this should
    be a general purpose thing so I'll leave the
    more complex code in for now.
    """
    assert str(cond.operation) == "="
    result = [x for x in series if getattr(x, cond.left.name) == cond.right]

    # error reporting:
    klass = series.type.__name__
    where = "where %s %s %s" % (cond.left.name, cond.operation, cond.right)
    assert len(result) >  0, "no %s found %s" % (klass, where)
    assert len(result) == 1, "found more than one %s %s" % (klass, where)

    return result[0]

# and here's the payoff :)
    
def safeDomain(user, domName):
    return only(user.domains,  where(Domain.domain) == domName)

def safeEmailRule(domain, virtuser):
    return only(domain.rules, where(EmailRule.virtuser) == virtuser)

def safeEmailRuleByID(domain, ID):
    return only(domain.rules, where(EmailRule.ID) == int(ID))

def safeMailbox(user, mailbox):
    return only(user.boxes, where(Mailbox.mailbox) == mailbox)

def safeSite(user, ID):
    return only(user.sites, where(Site.ID) == int(ID))

def safeSiteByName(user, domName):
    return safeDomain(user, domName).site

def safeDNSRec(domain, ID):
    return only(domain.dnsrecs, where(DNSRec.ID) == int(ID))

def safeDb(user, dbname):
    return only(user.dbs, where(Database.dbname)==dbname)
