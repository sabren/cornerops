from cornerhost.schema import User, Domain, Plan, Signup
from cornerhost.config import schema
from cornerhost import AdminApp
from clerks import MockClerk
from cornerhost.features import admin
from weblib import Redirect
import unittest

class AdminAppTest(unittest.TestCase):

    def setUp(self):
        self.clerk=MockClerk(schema)
        self.app = AdminApp(User(), self.clerk)
        self.sess = {"username":"fred"}
                    
        
    def test_UpdateUserCommand(self):
        fred = self.clerk.store(User(username="fred"))
        script = self.clerk.store(Plan(name="script"))

        cmd = admin.UpdateUserCommand(self.clerk)
        req = {
            'status':'locked',
            'plan':'script',
            'diskextra':'10',
            'bandextra':'20',
            'boxextra':'0',
            'dbextra':'0',
            '_clerk': self.clerk,
            '_sess': self.sess,
        }
        self.assertRaises(Redirect, cmd.invoke,  **req)
        assert fred.status == req['status']
        assert fred.plan.name == req['plan']
        assert fred.diskextra == int(req['diskextra'])
        assert fred.bandextra == int(req['bandextra'])

    def test_IsPasswdCommand(self):
        
        u = self.clerk.store(User(username="fred"))
        
        class MockBeaker:
            def ispasswd(self, username, password): return True
        class MockUser(User):
            def ispasswd(self, pwd): return pwd=="good"
        def mockLoadUser(u,c):
            return MockUser()

        cmd = admin.IsPasswdCommand(self.clerk)
        cmd.loadUser = mockLoadUser
        
        model = cmd.invoke(self.clerk, u, password="good")
        assert model["message"]=="yes"
        model = cmd.invoke(self.clerk, u, password="bad")
        assert model["message"]=="no"

    def test_JumpCommand(self):
        
        wanda = User(username="wanda")
        wanda.domains << Domain(domain="wtempy.com")
        self.clerk.store(wanda)

        invoke = lambda jumpto: (
            cmd.invoke(_sess=self.sess, _clerk=self.clerk, jumpto=jumpto))

        # searching for wanda should succeed:
        cmd = admin.JumpCommand(self.clerk)
        self.assertRaises(Redirect, invoke, jumpto="wanda")
        assert self.sess["username"] == "wanda"

        # but since there's no one else, another search should fail:
        self.assertRaises(AssertionError, invoke, jumpto="invalid")

        # you should also be able to look her up by domain:
        del self.sess["username"]
        self.assertRaises(Redirect, invoke, jumpto="wtempy.com")
        assert self.sess["username"] == "wanda"        

    def test_ReviewSignup(self):
        
        newbie = Signup(username="newbie")
        self.clerk.store(newbie)

        cmd = admin.ReviewSignup(self.clerk)
        model = cmd.invoke(self.clerk, ID=newbie.ID)
        assert model.signup.username=="newbie"

        
if __name__=="__main__":
    unittest.main()
    
