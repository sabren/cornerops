__ver__="$Id: Domain.py,v 1.10 2007/04/20 09:31:00 sabren Exp $"
import cornerhost
import re
from cornerhost.schema import EmailRule, DNSRec, Site
from strongbox import *

from EmailRule import reDefault, reBounce, rePopBox
from pytypes import EmailAddress
reRewrite = r"(%1|%2|%3|\w|-|\+)+(\.|%1|%2|%3|\w|-|\+)*@(\w|-)+(\.(\w|-)+)+"
reCatchall  = re.compile("^%s$" % "|".join([reDefault, reBounce, rePopBox, reRewrite]))
reEmail = re.compile(EmailAddress.regex)

reDomain = re.compile(
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
                    okay=lambda s: (not s) or reDomain.match(s.lower()))
    mailto = attr(str, default=EmailRule.BOUNCE)
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
        if reDomain.match(value):
            self.private.domain = value.lower()
        else:
            raise ValueError("invalid domain: %s" % value)
        self.onSet("domain", value)

    def set_mailto(self, value):
        """
        allow rewrite rules for sendmail but NOT normal forwards.
        """
        if reCatchall.match(value):
            if reEmail.match(value):
                pass # raise ValueError("catchall", "Forwarding is prohibited.")
            self.private.mailto = value
            self.onSet("mailto", value)
        else:
            raise ValueError("catchall", "invalid catchall: %s" % value)

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
