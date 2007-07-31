__ver__="$Id: Database.py,v 1.2 2006/07/02 05:33:08 sabren Exp $"
from strongbox import *
import cornerhost

class Database(Strongbox):
    ID = attr(long)
    dbname = attr(str, okay=r"^\w+_\w+$", allowNone=False)
    user = link(lambda : cornerhost.User)
