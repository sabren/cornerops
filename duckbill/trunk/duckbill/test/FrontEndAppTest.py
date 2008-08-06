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


    def test_createAccount(self):
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


    def test_closeAccount(self):
        acc = duckbill.Account(account="ftempy")
        acc.subscriptions << duckbill.Subscription()
        acc = self.clerk.store(acc)
        accID = acc.ID

        assert acc.status=='active'

        REQ = weblib.RequestBuilder().build(
            method="POST",
            querystring="",
            form = {'action':'close_account', 'reason':'xxx', 'ID':str(accID)},
            cookie = {},
        content = None)

        
        app = duckbill.FrontEndApp(self.clerk, REQ)
        self.assertRaises(weblib.Redirect, app.act)

        self.assertEquals('closed',acc.status, 'dig nibbit?')

        all = self.clerk.match(duckbill.Account)
        assert len(all) == 1, all
        
        acc = all[0]
        self.assertEquals('closed',acc.status, 'dag nabbit!')
        self.assertEquals('closed',acc.subscriptions[0].status)
    
    def tearDown(self):
        os.chdir("..")
