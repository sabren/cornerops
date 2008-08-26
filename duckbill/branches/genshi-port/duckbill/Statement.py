import duckbill
from pytypes import Date

class Statement:
    """
    Statement of an account for a particular time
    """
    __ver__="$Id: Statement.py,v 1.9 2003/03/14 04:39:41 sabren Exp $"

    __props = ("events", "openBal", "closeBal", "start", "end")

    def __init__(self, acc, start=None, end=None):
        self.acc = acc
        self.start = start or acc.opened.toUS() 
        self.end = end or Date("today")

    def get_openBal(self):
        return self.acc.balance(self.start)

    def get_closeBal(self):
        return self.acc.balance(self.end)

    def get_start(self):
        return self.start.toUS()
    
    def get_end(self):
        return self.end.toUS()

    def get_events(self):
        return self.acc.eventsBetween(self.start, self.end)

    def __getattr__(self, attr):
        # I'm a proxy, baby...
        if attr in self.__props:
            return eval("self.get_%s()" % attr)
        else:
            return getattr(self.acc, attr)


    ## make it a dict for zebra:
    ## @TODO: rethink all this...
    def keys(self):
        return self.__props + ("account",)
    def __getitem__(self, item):
        return getattr(self, item)


