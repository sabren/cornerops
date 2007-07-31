
import unittest
from cornerhost import Signup
from clerks import MockClerk
from duckbill import Subscription, Event

class SignupTest(unittest.TestCase):

    def test_toDuckbill(self):       
        p = Signup(
                fname="fred",
                lname="tempy",
                username="ftempy",
                plan="basic",
                cycLen="year")
        a = p.toDuckbill()
        assert a.account == "ftempy"
        assert a.fname == "fred"
        assert a.lname == "tempy"
        assert a.brand == "cornerhost"
        assert len(a.subscriptions) == 1
        assert a.subscriptions[0].username == "ftempy"
        assert a.events[0].amount == 50
        assert a.balance() == 50, a.balance()
        assert a.cycLen == "month" # billing is always monthly!
        assert a.subscriptions[0].cycLen=="year"


if __name__=="__main__":
    unittest.main()
    
