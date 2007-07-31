__ver__="$Id: MailboxTest.py,v 1.3 2005/06/23 04:59:18 sabren Exp $"
import unittest
from cornerhost.schema import Mailbox

class MailboxTest(unittest.TestCase):

    def test_validation(self):
        assert Mailbox(mailbox="pop_asdf_z09"), "should be ok"
        self.assertRaises(ValueError, Mailbox, mailbox="not_pop")
        self.assertRaises(ValueError, Mailbox, mailbox="pop_ with space")
        self.assertRaises(ValueError, Mailbox, mailbox="pop_$justEvil")
        self.assertRaises(ValueError, Mailbox, mailbox="pop_&justEvil")
        self.assertRaises(ValueError, Mailbox, mailbox="pop_UpperCase")
        self.assertRaises(ValueError, Mailbox, mailbox=None)

if __name__=="__main__":
    unittest.main()

