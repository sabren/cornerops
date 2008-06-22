__ver__="$Id: EmailRule.py,v 1.6 2006/07/02 05:33:08 sabren Exp $"
from strongbox import *
from pytypes import EmailAddress
import cornerhost

assert EmailAddress.regex[0]=="^"
assert EmailAddress.regex[-1]=="$"
reForward = EmailAddress.regex[1:-1]

reDefault = r'~'
reAlias  = r'alias_(\w|-)+'
rePopBox = r'pop_(\w|-)+'
reBounce = r'error:nouser'

reEmailRule = "^%s$" % "|".join([reDefault, reBounce, rePopBox, reForward, reAlias])


class EmailRule(Strongbox):
    BOUNCE = "error:nouser"
    ID = attr(long)
    # http://www.remote.org/jochen/mail/info/chars.html
    virtuser = attr(str, okay=r"^(\.?[\+\-A-Za-z0-9_]+)*$", )
    mailto = attr(str, okay=reEmailRule, default=reDefault)
    domain = link(lambda : cornerhost.Domain)
