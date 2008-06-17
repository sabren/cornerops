"""
test cases for duckbill.FrontEndApp
"""
__ver__="$Id: FrontEndAppTest.py,v 1.11 2006/07/02 06:08:09 sabren Exp $"

import unittest
import duckbill
import weblib
from clerks import MockClerk
from duckbill.config import schema
import os



class FrontEndAppTest(unittest.TestCase):

    def setUp(self):
        self.clerk = MockClerk(schema)
        os.chdir("frontend")
        self.app = duckbill.FrontEndApp(self.clerk, {})
        self.app.debug = 1


    def check_createAccount(self):
        # test to expose a bug... all this SHOULD do is show a form..
        #@TODO: will need to clean this up once weblib refactoring is done
        REQ = weblib.RequestBuilder().build(
            method="GET",
            querystring="action=create&what=account",
            form = {},
            cookie = {},
        content = None)
        app = duckbill.FrontEndApp(self.clerk, REQ)
        app.act()
    
    def tearDown(self):
        os.chdir("..")
