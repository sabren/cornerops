import unittest
from clerks import MockClerk, Schema
from cornerhost import Site, Domain, User, Server, UserApp
from cornerhost.dbmap import DBMAP
import personas

class UserAppTest(unittest.TestCase):

    def test_constructor(self):
        app = UserApp(User(), MockClerk(DBMAP), sess={})

if __name__=="main":
    unittest.main()
