import duckbill
from pytypes import Date
from strongbox import attr, Strongbox

class Cycle(object):
    def __init__(self, cyclicInstance):
        self.cyclic = cyclicInstance
    def __repr__(self):
        return "%s()" % self.__class__.__name__ # really just for testing
    def nextDue(self):
        raise NotImplementedError, "use XXXXCycle instead"

class MonthlyCycle(Cycle):
    def nextDue(self):
        nd = self.cyclic.nextDue
        if nd is None:
            return None
        else:
            return nd + nd.daysInMonth()

class YearlyCycle(Cycle):
    def nextDue(self):
        nd = self.cyclic.nextDue
        if nd is None:
            return None
        else:
            # make copy, inc year + return
            # this handles leap years correctly.
            cp = nd + 0
            cp.y += 1
            return cp

 
class Cyclic(Strongbox):
    """
    Mixin class for cyclic behavior.
    By default, this uses a monthly cycle.

    Classes that use this should assign nextDue
    in their constructors.
    """
    __ver__="$Id: Cyclic.py,v 1.15 2007/03/30 00:29:18 sabren Exp $"

    nextDue = attr(Date)
    cycLen = attr(str, okay=["month", "year"], default="month")

    def get_cycle(self):
        if self.cycLen == "year":
            return YearlyCycle(self)
        else:
            return MonthlyCycle(self)

    def calcNextDue(self):
        """
        Returns one month after current due date.
        """
        return self.get_cycle().nextDue()

    def isDue(self):
        # note that we use duckbill.TODAY rather than TODAY
        # so we can test more easily.
        # @TODO: this really ought to call a function,
        # even for testing... (???)
        return (self.nextDue is not None) \
               and (self.nextDue <= duckbill.TODAY)

    def catchup(self):
        wasDue = 0
        while self.isDue():
            wasDue = 1
            self.onDue()
            self.nextDue = self.calcNextDue()
        self.onCatchup(wasDue)

            
    ## events #################################################

    def onDue(self):
        pass

    def onCatchup(self, wasDue):
        pass
