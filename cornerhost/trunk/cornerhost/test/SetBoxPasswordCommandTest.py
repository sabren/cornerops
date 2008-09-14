import unittest
import personas
from cornerhost.features import email
from cornerhost.schema import Mailbox

class SetBoxPasswordCommandTest(unittest.TestCase):

    def setUp(self):
        self.uc = personas.fredClerk()
        self.cmd = email.SetBoxPasswordCommand()
        self.box = "pop_fred_box"
        self.uc.user.boxes << Mailbox(mailbox=self.box)
        self.uc.clerk.store(self.uc.user)
        self.invoke = lambda mailbox,pass1,pass2: (
            self.cmd.invoke_x(self.uc.user, mailbox, pass1, pass2))
        

    def test_nonexistent_box(self):
        self.assertRaises(LookupError, self.invoke,
                          mailbox="pop_fake_box",
                          pass1="asdf",
                          pass2="asdf")
        
    def test_stolen_box(self):
        wanda = personas.makeWanda(self.uc.clerk)
        wanda.boxes << Mailbox(mailbox="pop_wanda_asdf")
        self.uc.clerk.store(wanda)
        self.assertRaises(LookupError, self.invoke,
                          mailbox="pop_wanda_asdf",
                          pass1="asdf",
                          pass2="asdf")

    def test_null_password(self):
        self.assertRaises(ValueError, self.invoke,
                          mailbox=self.box,
                          pass1="",
                          pass2="")

    def test_mismatched_passwords(self):
        self.assertRaises(ValueError, self.invoke,
                          mailbox=self.box,
                          pass1="abc",
                          pass2="not the same")

    def test_remote_exception(self):
        self.assertRaises(IOError, self.invoke,
            mailbox= self.box,
            pass1 = "fail",
            pass2 = "fail")

if __name__=="__main__":
    unittest.main()
