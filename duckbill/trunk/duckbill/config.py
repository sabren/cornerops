"""
duckbill configuration file.
modify this to fit your own site and table names.
"""
from clerks import Clerk, Schema
from storage import MySQLStorage
from duckbill import *

# make this public key available to the user running duckbill:
GNUPG_RECIPIENT="billing@sabren.com"

schema = Schema({
    #Customer: "bill_customer",
    #Customer.accounts: (Account, "customerID"),
    Account: "bill_account",
    Subscription: "bill_subscription",
    Subscription.account: "accountID",
    Event: "bill_event",
    Event.account: "accountID",  
})


def makeClerk():
    import sqlCornerhost
    return Clerk(MySQLStorage(sqlCornerhost.connect()), schema)
