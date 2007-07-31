
__ver__="$Id: Usage.py,v 1.2 2006/07/02 05:33:08 sabren Exp $"
from strongbox import *
from pytypes import Date


class Usage(Strongbox):
    ID = attr(long)
    user = link(lambda : cornerhost.User)
    whichday = attr(Date)
    traffic = attr(long)
    
