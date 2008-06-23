
import unittest
from cornerhost.schema import EmailRule

class EmailRuleTest(unittest.TestCase):

    def test_defaults(self):
        e = EmailRule()
        assert e.mailto == EmailRule.DEFAULT == "~"

    def test_regexp(self):
        """
        There's a list of valid email characters here, based
        on the RFC:
        
        http://www.remote.org/jochen/mail/info/chars.html

        Basically this test just duplicates that table,
        and then loops through and tries every single
        character to make sure it works as specified for
        both the virtuser and the mailto.

        We're paranoid, so anything marked 'maybe' is
        disallowed.
        """
      
        ranges= {
            (0x00, 0x2B) : False,  # control chars, space, !"#$%&'()*
            (0x2b, 0x2C) : True,   # +
            (0x2C, 0x2D) : False,  # ,
            (0x2D, 0x2F) : True,   # - .
            (0x2F, 0x30) : False,  # /
            (0x30, 0x3A) : True,   # 0-9
            (0x3A, 0x41) : False,  # :;<=>?@
            (0x41, 0x5b) : True,   # A-Z
            (0x5b, 0x5f) : False,  # [\]^
            (0x5f, 0x60) : True,   # _
            (0x60, 0x61) : False,  # `
            (0x61, 0x7b) : True,   # a-z
            (0x7b, 0xff) : False,  # everything else
        }
        for (start, stop), okay in ranges.items():
            for code in range(start, stop):
                char = chr(code)
                
                gotError = False
                try:
                    rule = EmailRule(virtuser="a%sz" % char)
                except:
                    gotError = "virtuser"

                try:
                    rule = EmailRule(mailto="a%sz@xyz.com" % char)
                except:
                    gotError = "mailto"

                    
                if okay:
                    assert not gotError, "should have allowed '%s'" % char
                else:
                    assert gotError, "should not have allowed '%s'" % char
                
            
    def test_doubledots(self):
        try:
            EmailRule(virtuser='x..y')
        except ValueError:
            pass
        else:
            assert "should fail on double dots"


    def test_emailRE(self):
        # this was just sitting and spinning
        # because the regexp was so slow:
        EmailRule(mailto='alias_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # and then this failed!!
        EmailRule(mailto='aaa.bbb@ccc.ddd')

        # another regression test (because of the +)
        EmailRule(mailto='a.b+c@e.d')
            


if __name__=="__main__":
    unittest.main()
