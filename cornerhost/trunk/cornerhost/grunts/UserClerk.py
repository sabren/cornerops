from cornerhost.schema import DNSRec, Domain, Site, User, EmailRule
from clerks import Clerk

#@TODO: see if this can be replaced, given cornerhost.safety

class UserClerk:
    """
    I make sure users can only access their own objects.
    """
    def __init__(self, user, clerk):
        if not isinstance(user, User):
            raise TypeError('user',(type(user)))
        if not isinstance(clerk, Clerk):
            raise TypeError('clerk', type(clerk))
        self.user = user
        self.clerk = clerk

    def safeDomain(self, domainName):
        try:
            dom = self.clerk.fetch(Domain, domain=domainName)
            assert dom.user is self.user, "invalid domain: %s" % domainName
        except LookupError:
            raise AssertionError, "invalid domain: %s" % domainName
        else:
            return dom

    def safeDNSRec(self, ID):
        if ID:
            try:
                rec = self.clerk.fetch(DNSRec, ID=ID)
                assert rec.domain.user is self.user, "not your record"
                return rec
            except LookupError:
                #@TODO: I don't like this raise AssertionError crap:
                raise AssertionError, "couldn't load record"
        else:
            # set to dummy domain that gets discarded later
            return DNSRec(domain=Domain(domain='dummy.domain'))
        
    def safeSite(self, ID):
        msg = "unable to load site object"
        try:
            site = self.clerk.fetch(Site, ID=ID)
        except LookupError:
            raise AssertionError(msg)
        else:
            assert site.user is self.user, msg
        return site

    def safeSiteByName(self, domName):
        return self.safeDomain(domName).site       

    def safeEmailRule(self, ID):
        if ID:
            rule = self.clerk.fetch(EmailRule, ID=ID)
            assert rule.domain.user is self.user, "not your rule"
            return rule
        else:
            return EmailRule()
        
