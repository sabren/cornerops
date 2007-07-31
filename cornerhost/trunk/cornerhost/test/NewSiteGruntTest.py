__ver__="$Id: NewSiteGruntTest.py,v 1.20 2006/07/02 05:33:08 sabren Exp $"
import unittest
from clerks import MockClerk, Schema
from storage import MockStorage
from cornerhost import *
from cornerhost.remote import MockBeaker

class NewSiteGruntTest(unittest.TestCase):

    def setUp(self):
        self.clerk = MockClerk(Schema(cornerhost.config.DBMAP))
        self.user = self.clerk.store(User(username="ftempy",
                                          server=Server(name="mockium")))

    def makeGrunt(self):
        return NewSiteGrunt(self.clerk, self.user)

    def test_storage(self):       
        g = self.makeGrunt()
        assert g.user.username == "ftempy"
        assert g.user.ID == 1
        g.addDomain("ftempy.com")
        d = self.clerk.fetch(Domain, 1)
        assert d.domain == "ftempy.com", "Domain record didn't get saved!"
        assert d.user.ID == 1, "didn't store domain.user.ID: %s" % d.user.ID
        assert d.ID == 1
        assert d.site is None
        
        self.makeGrunt().addSite("ftempy.com")
        sites = self.clerk.match(Site)
        assert len(sites)== 1, "expectedd 1 site, got %s" % len(sites)
        s = sites[0]
        assert s.domain.ID==1, "wrong domainID: %s" % s.domain.ID
        assert s.user.ID == 1, "didn't store site.user.ID: %s" % s.user.ID
        assert s.ID == 1

        d = self.clerk.fetch(Domain, 1)
        assert d.site.ID == 1, "didn't update domain.site.ID"

    def test_makeDirs(self):
        "it should just pass the call the the appropriate beaker"
        MockBeaker.log = []
        mk = MockBeaker()
        self.makeGrunt().makeDirs("ftempy.com")
        assert mk.log == ["makeSiteDirs('ftempy','ftempy.com') "], \
               "didn't relay makesite request to beaker!: %s" % mk.log

    def test_checkDomain(self):
        c = self.clerk
        def fails(d):
            try: self.makeGrunt().checkDomain(d)
            except ValueError: return True

        # invalid domains should fail:
        assert fails("sabren..com")

        # should fail if domain in the system:
        assert not fails("ftempy.com")
        u = c.fetch(User,1)
        u.domains << Domain(domain="ftempy.com")
        c.store(u)
        
        assert fails("ftempy.com")   

        # www indicates subdomains, which we don't allow yet!
        assert fails("www.wtempy.com")

        # another subdomain check:
        assert not fails( "sub.rufustempy.com")
        assert fails("sub.ftempy.com")

        # finally, disallow *.sabren.com wildcard sudomains:
        assert fails("ftempy.sabren.com")
        assert fails("ftempy.ab.sabren.com")
               

    def test_addSub(self):
        grunt = self.makeGrunt()

        try:
            grunt.addSub("sub","domain.com")
            gotError = 0
        except ValueError:
            gotError = 1
        assert gotError, "should have failed! - domain.com is unknown"    

        # but if we add it:
        grunt.addDomain("domain.com")
        # have to reload ftempy though:
        grunt = self.makeGrunt()
        grunt.addSub("sub","domain.com")
        

        # now make sure it got saved:        
        d =  self.clerk.match(Domain,domain="sub.domain.com")[0]
        assert d.rectype=="cname"
        assert d.location=="domain.com"
        assert d.zone.domain == "domain.com"
        assert d.user.ID == 1
        assert not d.processmail

        # and make sure we can't add subs to subs
        # (instead just make a new subdomain with a dot in it)
        try:
            grunt = self.makeGrunt()
            grunt.addSub("sub","sub.domain.com")
        except:
            pass
        else:
            self.fail("should fail when nesting subdomains")
            
