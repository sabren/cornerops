"""
test cases for Statement
"""
__ver__="$Id: StatementTest.py,v 1.5 2002/05/28 07:30:40 sabren Exp $"

import unittest
import duckbill
from duckbill import Statement
from duckbill import Event
from pytypes import DateTime
from pytypes import Date

from duckbill import Account
from duckbill.test import FIRST_STATEMENT_DATE
from duckbill.test import FIRST_STATEMENT_AMOUNT
from duckbill.test import CUSTOMER_SIGNUP_DATE

class StatementTest(unittest.TestCase):

    def setUp(self):
       self.acc = Account()
        
    # both of these work the same way. real magic is in
    # account.balance()
    def test_openBalance(self):

        assert Statement(self.acc).openBal == 0
        assert Statement(self.acc).closeBal == 0
        self.acc.events << duckbill.newEvent("charge", amount=5, posted=DateTime("now"))
        assert Statement(self.acc).openBal == 0, \
                "Expected opening balance of 0, got %s" % Statement(self.acc).openBal
        assert Statement(self.acc, start=Date("today"), end=Date("today")+1).closeBal == 5, \
                "Expected closing balance of 5, got %s" \
                % Statement(self.acc, end=Date("today")+1).closeBal


