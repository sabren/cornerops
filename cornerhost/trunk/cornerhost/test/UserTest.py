__ver__="$Id: UserTest.py,v 1.6 2006/07/02 05:33:08 sabren Exp $"
import unittest
import handy
from cornerhost.schema import User, Plan, Server
from duckbill import Account

class UserTest(unittest.TestCase):

    def test_account(self):
        u = User()
        u.account = Account()

    def test_diskquota(self):
        basic = Plan(diskquota = 100 * handy.MEGA)
        
        u = User(plan=basic)
        assert u.diskquota == 100 * handy.MEGA

        u.diskextra = 50 * handy.MEGA
        assert u.diskquota == 150 * handy.MEGA

    def test_bandquota(self):
        basic = Plan(bandquota =  2 * handy.GIGA)
        self.assertEquals(User(plan=basic).bandquota, 2 * handy.GIGA)

        shell = Plan(bandquota =  5 * handy.GIGA)
        self.assertEquals(User(plan=shell).bandquota, 5 * handy.GIGA)
        
    def test_bandrule(self):
        u = User()
        u.bandrule = "charge"
        u.bandrule = "disable"
        self.assertRaises(ValueError, u.__setattr__, *("bandrule", "garbage"))

    def test_bandquota(self):
        basic = Plan(boxquota =  2)
        self.assertEquals(User(plan=basic).boxquota, 2)
        self.assertEquals(User(plan=basic, boxextra=2).boxquota, 4)

    def test_dbquota(self):
        script = Plan(dbquota = 2)
        self.assertEquals(User(plan=script).dbquota, 2)
        self.assertEquals(User(plan=script, dbextra=2).dbquota, 4)

    def test_remote(self):
        s = Server(name="mockium")
        assert User(server=s).getMySQL()
        assert User(server=s).getBeaker()

if __name__=="__main__":
    unittest.main()

