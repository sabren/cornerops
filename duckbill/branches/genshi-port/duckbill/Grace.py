from pytypes import Date
from strongbox import *
import duckbill

class Grace(Strongbox):
    """
    Grace Period.
    """
    __ver__="$Id:$"

    ID = attr(long)
    account = link(lambda : duckbill.Account)
    expires = attr(Date, default=duckbill.TODAY+7)
    reason = attr(str)

    def hasExpired(self):
        return self.expires <= duckbill.TODAY

    def __str__(self):
        return 'graced until %s because %s' % (self.expires, self.reason)
