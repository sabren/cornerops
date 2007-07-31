__ver__="$Id: EmailRule.py,v 1.6 2006/07/02 05:33:08 sabren Exp $"
from strongbox import *
import cornerhost

class EmailRule(Strongbox):
    ID = attr(long)
    # http://www.remote.org/jochen/mail/info/chars.html
    virtuser = attr(str, okay=r"^(\.?[\+\-A-Za-z0-9_]+)*$", )
    mailto = attr(str, okay=cornerhost.emailRE, default='~')
    domain = link(lambda : cornerhost.Domain)
