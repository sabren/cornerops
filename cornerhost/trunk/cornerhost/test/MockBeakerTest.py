
from cornerhost.remote import MockBeaker
import unittest
import xmlrpclib

class MockBeakerTest(unittest.TestCase):

    def setUp(self):
        self.beak = MockBeaker()

    def test_makeSiteDirs(self):
        self.beak.makeSiteDirs('user','domain');

    def test_genmailconf(self):
        self.beak.genmailconf()

    def test_addnew(self):
        self.beak.addnew("plan","user")

    def test_mqsend(self):
        self.beak.mqsend("asdf")

    def test_genhttpconf(self):
        self.beak.genhttpconf()

    def test_ispasswd(self):
        assert self.beak.ispasswd("user","okay")
        assert not self.beak.ispasswd("user","fail")

    def test_setpasswd(self):
        assert self.beak.setpasswd("user","old","new") == "ok"
        self.assertRaises(xmlrpclib.Fault,
                          self.beak.setpasswd,
                          "user","fail","new")

    def test_getcron(self):
        assert self.beak.getcron("user") == "mock crontab for user"
        assert self.beak.getcron("asdf") == "mock crontab for asdf"

    def test_setcron(self):
        assert self.beak.setcron("user","asdf") == "mock setcron result"





if __name__=="__main__":
    unittest.main()
