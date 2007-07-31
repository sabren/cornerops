__ver__="$Id: DomainTest.py,v 1.11 2004/11/26 13:02:01 sabren Exp $"
import unittest
from cornerhost import Domain, Site

class DomainTest(unittest.TestCase):

    def test_validation(self):
        "Domain.domain should only accept well-formed domains"
        def shouldfail(name):
            try: Domain(domain=name)
            except ValueError: return True
        assert shouldfail("http://www.sabren.com/")
        assert shouldfail("sabren..com")
        assert shouldfail("$sabren.com")
        assert shouldfail(" sabren.com")
        assert shouldfail("sabren.com ")
        assert shouldfail("-sabren.com") # I think?
        assert not shouldfail("sabren.com")
        assert not shouldfail("sabren2.com")
        assert not shouldfail("sabren.co.uk")
        assert not shouldfail("sa-br-en.com")        
        assert not shouldfail("s.a.b.r.e.n.com")        
        assert not shouldfail("sub.domain.sabren.com")
        assert Domain(domain="sabren.com").domain == "sabren.com"
        assert Domain(domain="SaBReN2.COM").domain == "sabren2.com"
                          
        # finally, this is a crazy one. It's for wildcard domains.
        assert not shouldfail("*.sabren.com")
        assert shouldfail("s*bren.com")
        assert shouldfail("xyz.*.com")
        assert shouldfail("*.*.com")
        assert shouldfail("*.*.xyz.com")        
        # this one is probably valid, but i don't like it:
        assert shouldfail("abc.*.sabren.com")

    def test_is_site(self):
        dom = Domain(domain="asdf.com")
        assert not dom.is_site
        dom.site = Site(domain=Domain(domain="main.com"))
        assert not dom.is_site
        dom.site = Site(domain=dom)
        assert dom.is_site
        

    def test_location(self):
        Domain(location='xyz.com')
        Domain(location='abc.xyz.com')
        Domain(location='127.0.0.1')
        try:
            Domain(location='xyz')
            self.fail('should have gotten valueError')
        except ValueError:
            pass


    def test_mailto(self):
        self.assertRaises(ValueError, Domain, mailto="e@p")
        
