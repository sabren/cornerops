__ver__="$Id: Domain.py,v 1.10 2007/04/20 09:31:00 sabren Exp $"
from cornerhost import emailRE
from cornerhost.schema import EmailRule, DNSRec, Site
import cornerhost
from strongbox import *
import re

domainRE = re.compile(
    """
    ^(\*\.)?         # optionally start wildcard
     (\w(-|\w)*\.)+  # followed by at least one non-wildcard chunk
    \w+$             # and then something like com/org/uk/etc
    """, re.VERBOSE | re.UNICODE)

class Domain(Strongbox):
    ID = attr(long)
    domain = attr(unicode)
    rule = attr(str, okay=['host','point','friend'], default='host')
    rectype = attr(str, okay=["a","cname","friend"], default="a")
    location = attr(str, default="",
                    okay=lambda s: (not s) or domainRE.match(s.lower()))
    mailto = attr(str, okay=emailRE, default='~')
    processmail = attr(int, okay=[0,1], default=1)
    rules = linkset(EmailRule, "domain")
    dnsrecs = linkset(DNSRec, "domain")
    site  = link(Site)
    user = link(lambda : cornerhost.User)
    zone = link(lambda : cornerhost.Domain)
    subs = linkset((lambda : cornerhost.Domain), "zone")

    def __init__(self, singleparam=None, **kw):
        if singleparam:
            kw["name"] = singleparam
        super(Domain, self).__init__(**kw)

    def get_prefix(self):
        if self.zone:
            return self.domain[:-len(self.zone.domain)-1]
        else:
            return self.domain

    def set_domain(self, value):
        if type(value) not in (str, unicode):
            raise TypeError('Domain.name', value)
        if domainRE.match(value):
            self.private.domain = value.lower()
        else:
            raise ValueError, "invalid domain: %s" % value
        self.onSet("domain", value)

    def get_is_site(self):
        return (self.site is not None) and (self.site.domain is self)
    
    def get_name(self):
        return self.domain
    def set_name(self, value):
        self.domain = value

    def get_catchall(self):
        class CatchAll:
            def getSlots(self): return self.__dict__.items()
        rule = CatchAll()
        rule.domain = self
        rule.mailto = self.mailto
        rule.virtuser = '(catchall)'
        return rule
