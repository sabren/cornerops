import unittest
import personas
from platonic import Intercept
from cornerhost.features import remote

class RemoteFeaturesTest(unittest.TestCase):
    #@TODO: add test cases for remote features

    def setUp(self):
        self.uc = personas.fredClerk()

    def test_CreateDatabaseCommand(self):
        fred = self.uc.user
        u,c = self.uc.user, self.uc.clerk
        
        cmd = remote.CreateDatabaseCommand(self.uc)

        #@TODO: instead of intercept, raise a specific error
        #(that can be mapped to Intercept in a generic way)

        # dbname must be filled in:
        self.assertRaises(TypeError, cmd.invoke)
        
        # dbname must be valid (bad_name is harcoded to fail in MockMySQL)
        self.assertRaises(Intercept, cmd.invoke, u,c, dbname="bad_name")
        
        assert fred.username == "fred"
        cmd.invoke(u,c, dbname='fred_db')
        assert fred.getMySQL().dbs[fred.username] == ["fred_db"]

    def test_SetMySQLPasswordCommand(self):
        cmd = remote.SetMySQLPasswordCommand(self.uc)
        self.assertRaises(Intercept, cmd.invoke,
                          new1="a'b", new2="a'b")
        cmd.invoke(new1="ab",new2="ab")
        assert self.uc.user.getMySQL().pwd['fred'] == "ab"


    def test_SetCronCommand(self):
        cmd = remote.SetCronCommand(self.uc)
        cmd.invoke(crontab="test_needline")
        fred = self.uc.user
        self.assertEquals("test_needline\n", fred.getBeaker().crontab)
        cmd.invoke(crontab="test_okay\n")
        self.assertEquals("test_okay\n", fred.getBeaker().crontab)

if __name__=="__main__":
    unittest.main()

