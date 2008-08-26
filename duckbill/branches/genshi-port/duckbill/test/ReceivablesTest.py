"""
test cases for Receivables
"""
__ver__="$Id: ReceivablesTest.py,v 1.3 2006/07/02 06:08:09 sabren Exp $"
import unittest

class ReceivablesTest(unittest.TestCase):

    # i don't really know what to test here.
    # all it does is run a hardcoded SQL
    # query to get due accounts (which is
    # basically a kluge because clerks doesn't
    # support that kind of query and it's DAMN
    # slow if I don't filter out paid accounts)
    #
    # Then it just loops through the accounts
    # and calls the aging routine that Account
    # already has.
    #
    # So basically there's not much to test
    # right now, especially since I already
    # had the code written a long time ago.
    #
    # <shrug> :)
    pass
