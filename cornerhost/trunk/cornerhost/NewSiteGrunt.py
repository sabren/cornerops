__ver__="$Id: NewSiteGrunt.py,v 1.17 2004/11/26 10:13:40 sabren Exp $"
import cornerhost
from cornerhost import User, Site, Domain, Server
from pytypes import DateTime

class NewSiteGrunt(object):
    """
    I manage the creation of new sites/domains.
    """
    ERR = {
        "www": ("'www' prefix not allowed here." 
                "(www aliases are created automatically)"),
        "dup": "%s is already in the system",
        "sub": "subdomains not working yet!",
        "sei": "*.sabren.com domains cannot be added from here.",
        "dad": "please add %s to your account first",
        "zon": "can't add subdomain to a subdomain",
    }    
    
    def __init__(self, clerk, user, sabrenOK=False):
        self.clerk = clerk
        assert isinstance(user, User), "NewSiteGrunt takes a User object now"
        self.user = user
        self.log = ""
        self.sabrenOK = sabrenOK

    def newSite(self, domain):
        """
        main template method
        """
        self.addDomain(domain)
        self.buildSite(domain)

    def newSiteForSubdomain(self, sub, domain):
        self.addSub(sub, domain)
        self.buildSite(sub + "." + domain)      

    def buildSite(self,domain):
        """
        adds site for existing domain, creates directories
        """
        s = self.addSite(domain)
        self.makeDirs(domain)
        self.user.getBeaker().mqsend('genhttpconf')
        return s

    def checkDomain(self, domain, subsokay=0):
        """
        System-level validation of the domain name.
        """
        # first run it through Domain's validation:
        # (also makes it lowercase, etc)
        domain = Domain(domain=domain).domain

        # now use the real stuff:
        if self.clerk.match(Domain, domain=domain):
            raise ValueError, self.ERR["dup"] % domain

        #if domain.startswith("www."):
        #    raise ValueError, self.ERR["www"]

        if not subsokay:
            for d in self.user.domains:
                if domain.endswith( "." + d.domain):
                    raise ValueError, self.ERR["sub"]

        if domain.endswith(".sabren.com") and not self.sabrenOK:
            raise ValueError, self.ERR["sei"]

        return domain # filtered for lowercase, etc..


    def addDomain(self, domain):
        d = Domain(domain=self.checkDomain(domain), user=self.user)
        self.user.domains << d
        return self.clerk.store(d)
        
    def addSub(self, sub, domain):
        match = [d for d in self.user.domains if d.domain==domain]
        if not match:
            raise ValueError, self.ERR["dad"] % domain
        parent = match[0]
        if parent.zone:
            raise ValueError, self.ERR["zon"] % domain
        sub = self.checkDomain(sub + "." + domain, subsokay=1)
        d = Domain(domain=sub,
                   user=self.user,
                   rectype="cname",
                   location=domain,
                   processmail=0,
                   zone=parent)
        return self.clerk.store(d)
        

    def addSite(self, domain):
        d = self.clerk.fetch(Domain, domain=domain)
        d.site = Site(domain=d, user=self.user)
        self.clerk.store(d)
        return d.site

    def makeDirs(self, domain):
        self._getBeaker().makeSiteDirs(self.user.username, domain)

    def _getBeaker(self):
        # factored out so we can override in tests
        return self.user.getBeaker()
