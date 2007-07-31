__ver__="$Id: UsageTest.py,v 1.4 2006/07/02 05:33:08 sabren Exp $"

import unittest
from cornerhost import User, Usage
from handy import MEGA, GIGA
from pytypes import PythonicRange, Date

class UsageTest(unittest.TestCase):

    def check_classes(self):
        usr = User()
        usg = Usage(whichday="today", traffic=25 * MEGA)
        usr.usage << usg

    def check_usage(self):
        period = PythonicRange(Date("today")-10, Date("today"))
        usr = User()

        # zero by default:
        assert usr.trafficUsed(period) == 0

        # sum the data:
        usr.usage << Usage(whichday=Date("today")-1, traffic=1*GIGA)
        usr.usage << Usage(whichday=Date("today")-2, traffic=1*GIGA)        
        assert usr.trafficUsed(period) == 2 * GIGA

        # ignore data out of range (note: it's a PythonicRange)
        usr.usage << Usage(whichday=Date("today"), traffic=1*GIGA)
        usr.usage << Usage(whichday=Date("today")-32, traffic=1*GIGA)        
        assert usr.trafficUsed(period) == 2 * GIGA


if __name__=="__main__":
    unittest.main()
