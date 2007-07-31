#@+leo

#@+node:0::@file StatementTest.py

#@+body
"""
test cases for Statement
"""
__ver__="$Id: StatementTest.py,v 1.5 2002/05/28 07:30:40 sabren Exp $"

import unittest
import duckbill.spec
from duckbill import Statement
from duckbill import Event
from pytypes import DateTime
from pytypes import Date

from duckbill import Account
from duckbill.spec import FIRST_STATEMENT_DATE
from duckbill.spec import FIRST_STATEMENT_AMOUNT
from duckbill.spec import CUSTOMER_SIGNUP_DATE

class StatementTest(unittest.TestCase):

    def setUp(self):
       self.acc = Account()
        
    # both of these work the same way. real magic is in
    # account.balance()
    def check_closeBalance(self): pass
    def check_openBalance(self):

        assert Statement(self.acc).openBal == 0
        assert Statement(self.acc).closeBal == 0
        self.acc.events << duckbill.newEvent("charge", amount=5, posted=DateTime("now"))
        assert Statement(self.acc).openBal == 0, \
                "Expected opening balance of 0, got %s" % Statement(self.acc).openBal
        assert Statement(self.acc, start=Date("today"), end=Date("today")+1).closeBal == 5, \
                "Expected closing balance of 5, got %s" % Statement(self.acc, end=Date("today")+1).closeBal


    def check_events(self):
        pass # this just calls account.eventsBetween(start, end)
#@-body

#@-node:0::@file StatementTest.py

#@-leo
