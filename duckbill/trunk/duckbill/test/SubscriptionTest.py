"""
test cases for Subscription
"""
__ver__="$Id: SubscriptionTest.py,v 1.7 2003/11/19 02:10:23 sabren Exp $"

import unittest
import duckbill
from pytypes import Date
from duckbill import Subscription, Account

from duckbill.spec import FIRST_STATEMENT_AMOUNT
from duckbill.spec import SECOND_STATEMENT_DATE
from duckbill.spec import CUSTOMER_SIGNUP_DATE

class SubscriptionTest(unittest.TestCase):

    def setUp(self):
        self.sub = duckbill.spec.fakeSubscription()
        self.today, duckbill.TODAY = duckbill.TODAY, CUSTOMER_SIGNUP_DATE

    #@TODO: move this to Cycle
    def test_calcCharge(self):
        """
        No prorating. Charge amount is the normal rate.
        """
        assert self.sub.calcCharge() == FIRST_STATEMENT_AMOUNT

    def test_simple(self):
        s = Subscription()
        s.service ='cat'

    def test_onDue(self):
        """
        onDue should post a charge and update nextDue.
        """
        self.sub = duckbill.spec.fakeSubscription()
        a = Account()
        self.sub.account = a
        self.sub.service = "service"
        self.sub.username = "username"
        self.sub.nextDue = CUSTOMER_SIGNUP_DATE
        assert len(a.events) == 0
        self.sub.catchup()
        assert len(a.events) == 1
        assert a.events[0].posted == CUSTOMER_SIGNUP_DATE
        assert a.events[0].maturity == SECOND_STATEMENT_DATE
        assert a.events[0].note == "1-month service [username]"
        assert self.sub.nextDue == SECOND_STATEMENT_DATE, self.sub.nextDue

    def tearDown(self):
        duckbill.TODAY = self.today
