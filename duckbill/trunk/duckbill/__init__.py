"""
duckbill - a python billing system
"""
__ver__="$Id: __init__.py,v 1.32 2006/07/02 06:08:09 sabren Exp $"
__release__="0.1"

from pytypes import Date, DateTime

TODAY = Date("today")
NOW = DateTime("now")

from Event import Event
from Grace import Grace
from Cyclic import Cyclic
from EncryptedCard import EncryptedCard
from Subscription import Subscription
from Statement import Statement
from Account import Account
from FrontEndApp import FrontEndApp
from Receivables import Receivables

import time
from decimal import Decimal
import config

#@TODO: consolidate this db map with the one in .weblib.py
dbTables = {
    Account: "bill_account",
    Subscription: "bill_subscription",
    Event: "bill_event",
}


def newEvent(event, acct=None, posted=None, note=None, amount=None):
    e = Event()
    e.account = acct or None
    e.event = event
    if type(posted) == type(""):
        e.posted = DateTime(posted)
    elif isinstance(posted, DateTime) or isinstance(posted, Date):
        e.posted = posted
    elif not posted:
        e.posted = DateTime("now")
    else:
        raise TypeError, "Event posted with illegal DateTime type"
    e.amount = amount or Decimal("0.00")
    e.note = note or ""
    return e
