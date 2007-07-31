"""
test cases for Event
"""
__ver__="$Id: EventTest.py,v 1.6 2003/02/27 21:34:57 sabren Exp $"

import unittest
import duckbill
from duckbill import Event
from pytypes import FixedPoint

class EventTest(unittest.TestCase):

    def setUp(self):
        pass

    def check_amount(self):
        """
        amount should always be a fixedpoint or None
        """
        e = Event()
        e.amount = None
        assert e.amount is None # make sure no error trying FixedPoint(None)
        e.amount = 1

    def check_NoneAmount(self):
        e = Event()
        e.amount = None
        assert e.value == 0
        
