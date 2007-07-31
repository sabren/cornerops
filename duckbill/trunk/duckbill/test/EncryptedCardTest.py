"""
Test cases for EncryptedCard
"""
__ver__="$Id: EncryptedCardTest.py,v 1.4 2004/08/02 21:42:14 sabren Exp $"

import unittest
from duckbill import GnuPG
import duckbill.config
from duckbill import EncryptedCard
from pytypes import Date

## To pass this test, you will need to run the following command:
##    gpg --gen-key
## and create a key for: "encrypted.card.test@sabren.com"
## with this passphrase: "encrypted card test"
## @TODO: have GnuPG auto-make the testing key if not there :)

class EncryptedCardTest(unittest.TestCase):

    def setUp(self):
        duckbill.config.GNUPG_RECIPIENT = 'encrypted.card.test@sabren.com'

    def test_encryption(self):
        c = EncryptedCard(owner='fred tempy', expire='1/1/2000', number='1234')
        assert not c.isEncrypted()
        assert c.owner =='fred tempy'
        assert str(c).startswith("-----BEGIN PGP MESSAGE-----"), str(c)
        assert not c.isEncrypted()

        s = str(c)
        del c
        
        c = EncryptedCard(s)
        assert c.isEncrypted()
        # new instance should fail since it's encrypted:
        self.assertRaises(AttributeError, getattr, c, "owner")

        # witthout the right passphrase, it should still fail
        self.assertRaises(Exception, c.decrypt, "not-the-pass-phrase")
        self.assertRaises(AttributeError, getattr, c, "owner")

        # but if we have the passphrase, all is well:
        c.decrypt("encrypted card test")
        assert not c.isEncrypted()
        assert c.owner == 'fred tempy'
        assert c.number == '1234'
        assert c.expire == Date("1/1/2000")


        def gpgsame(a,b):
            A = a.split("==")[0]
            B = b.split("==")[0]

        #@TODO: I'd like this to be the same all the time,
        #but it isn't... need to nail down when exactly the
        #cipher should be regenerated...
        #import pdb; pdb.set_trace()
        #assert gpgsame(str(c), s), str(c) +  "\n##VS##\n" + s
        c.owner = 'wanda tempy'
        assert not gpgsame(str(c), s)
        
        # just to be safe, prevent decrypting twice:
        self.assertRaises(Exception, c.decrypt, "encrypted card test")

    def test_None(self):
        assert str(EncryptedCard(None)) == ""
        assert str(EncryptedCard("")) == ""


if __name__=="__main__":
    unittest.main()
