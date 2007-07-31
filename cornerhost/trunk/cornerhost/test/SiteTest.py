__ver__="$Id: SiteTest.py,v 1.5 2006/07/02 05:33:08 sabren Exp $"
import unittest
from cornerhost import Site, Domain, User
from cornerhost.config import schema
from clerks import MockClerk

class SiteTest(unittest.TestCase):

    def setUp(self):
        self.clerk = MockClerk(schema)

    def test_aliases(self):
        d = Domain(domain="test.com")
        s = Site(domain=d)
        d.site = s
        a = Domain(domain="alias.com")
        s.aliases << a
        self.clerk.store(s)
        self.clerk.store(d)        
        s = self.clerk.fetch(Site, ID=1)

        # @TODO: remove this once clerk injects live data
        for a in s.aliases:            
            if a.domain: pass
        
        assert a in s.aliases

    def test_main_domain_not_in_aliases(self):
        raise "skip"
        # @TODO: assert d not in s.aliases
        # It passes now but I don't know why!!
        

if __name__=="__main__":
    unittest.main()
