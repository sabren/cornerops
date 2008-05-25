from cornerhost.features import email
from cornerhost import EmailRule
from cornerhost import remote
from cornerhost.schema import Mailbox, Plan
from platonic import Intercept
import personas
import unittest

class EmailFeaturesTest(unittest.TestCase):
    #@TODO: add test cases for ALL features.email classes
    def setUp(self):
        self.uc = personas.fredClerk()
        self.user = self.uc.user
        self.clerk = self.uc.clerk
        self.dom = self.uc.user.domains[0]
        
    def test_SaveCatchallCommand(self):
        cmd = email.SaveCatchallCommand(self.uc)
        req = {
            '_user': self.user,
            '_clerk': self.clerk,
            'domName':'fred.com',
            'mailto':'someone@else.com', #@TODO: unhardcode magic name
            'rule':'forward' }
        self.assertRaises(Intercept, cmd.invoke, **req)
        req['mailto']='fred@okay.com'
        cmd.invoke(**req) # should work now
        
    def test_SaveRuleCommand(self):
        cmd = email.SaveRuleCommand(self.uc)
        req = {
            '_clerk': self.clerk, '_user': self.user,
            'ID': '1',
            'domName':'fred.com',          
            'mailto':'good@forward.com',
            'rule':'forward' }
        self.assertRaises(Intercept, cmd.invoke, **req)
        req['virtuser']='good'
        cmd.invoke(**req) # should work

    def test_SaveRuleCommand_new(self):
        ruleCount = len(self.dom.rules)
        cmd = email.SaveRuleCommand(self.uc)
        req = {
            '_clerk': self.clerk, '_user': self.user,            
            'ID': None,
            'virtuser': 'xyz',
            'domName':'fred.com',          
            'mailto':'whatever',
            'rule':'bounce' }
        cmd.invoke(**req)
        self.assertEquals(ruleCount + 1, len(self.dom.rules))

    def test_SaveRuleCommand_existing(self):
        ruleCount = len(self.dom.rules)
        # change the spam rule to report spam:
        cmd = email.SaveRuleCommand(self.uc)
        cmd.invoke(
            _clerk=self.clerk, _user=self.user,            
            ID=self.dom.rules[0].ID,
            virtuser='report',
            domName='fred.com',
            rule='forward',
            mailto='report@spamtrapper.com')
        self.assertEquals(ruleCount, len(self.dom.rules),
                          "rule count should not change")
        rules = self.uc.clerk.match(EmailRule)
        assert rules[0].virtuser == 'report'
        assert rules[0].mailto == 'report@spamtrapper.com'
        

    def test_DeleteRuleCommand(self):
        cmd = email.DeleteRuleCommand(self.uc)
        cmd.invoke(self.user, self.clerk,
                   oldDom='fred.com', ID=self.dom.rules[0].ID)

    def test_CreateBoxCommand(self):
        fred = self.uc.user
        sess = {}
        c = self.clerk
        u = fred
        
        # if no quota, go for it:
        fred.plan.boxquota = Plan.UNLIMITED
        self.uc.clerk.store(fred)        
        cmd = email.CreateBoxCommand(self.uc)
        cmd.invoke(c,u, sess, mailbox="pop_asdf")

        # make sure password gets stored in session
        self.assertEquals(sess[email.SessionFeature.passVar],
                          remote.MOCKPASSWD)


        # enforce boxquota
        fred.plan.boxquota = 1
        self.uc.clerk.store(fred)        
        self.assertRaises(AssertionError, cmd.invoke, c,u, sess, mailbox='')
        
        fred.boxextra = 10
        self.uc.clerk.store(fred)
        cmd.invoke(c,u, sess, mailbox="pop_ok")

        fred.plan.boxquota = Plan.FORBIDDEN
        self.uc.clerk.store(fred)
        self.assertRaises(AssertionError, cmd.invoke, c,u, sess, None)

        # bounceback on error
        fred.plan.boxquota = 100
        self.assertRaises(Intercept, cmd.invoke, c,u, sess, '') # no box name
        self.assertRaises(Intercept, cmd.invoke, c,u, sess, '34$ds') # bad name
        # duplicate box:
        dupe = "pop_dupe"
        cmd.invoke(c,u, sess, mailbox=dupe)
        self.assertRaises(Intercept, cmd.invoke, c,u, sess, dupe)

if __name__=="__main__":
    unittest.main()
