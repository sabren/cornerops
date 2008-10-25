
import duckbill
import strongbox

###[ shared spec stuff ]#############

CUSTOMER_SIGNUP_DATE = duckbill.Date("4/16/2000")
FIRST_STATEMENT_DATE = duckbill.Date("4/16/2000")
FIRST_STATEMENT_AMOUNT = 10 # 5 for prorating
SECOND_STATEMENT_DATE = duckbill.Date("5/16/2000")
ANY_DATE = duckbill.Date("8/20/1976") # when we don't care what day it is

DAY_BEFORE_SIGNUP = duckbill.Date("4/15/2000") #@TODO: Date() - 1
DAY_AFTER_STATEMENT = duckbill.Date("5/2/2000")

def fakeAccount():
    return duckbill.Account(account="duckbill.spec account")

def fakeSubscription():
    return duckbill.Subscription(service='blog', username='ftempy',
                                 rate='10.00')
