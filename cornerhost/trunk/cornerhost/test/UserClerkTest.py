import unittest
from cornerhost import User, Server, Site, Domain, DNSRec, EmailRule
from cornerhost.grunts import UserClerk
from cornerhost.config import schema
from clerks import MockClerk
import personas

class UserClerkTest(unittest.TestCase):
    def setUp(self):
        clerk = MockClerk(schema)
        self.fred = personas.makeFred(clerk)
        self.uclerk = UserClerk(self.fred, clerk)

    #@TODO: def test_safeDomain(self):
    #@TODO: def test_safeDNSRec(self):
    #@TODO: def test_safeSite(self):

    def test_safeEmailRule_new(self):
        rule = self.uclerk.safeEmailRule(None)
        assert rule.ID == 0, rule.ID

    def test_safeEmailRule_existing(self):
        rID = self.fred.domains[0].rules[0].ID
        rule = self.uclerk.safeEmailRule(rID)
        self.assertEquals(rule.ID, rID)
        self.assertEquals(rule.virtuser, 'spam')
        self.assertEquals(rule.mailto, 'error:nouser')

        

if __name__=="__main__":
    unittest.main()
