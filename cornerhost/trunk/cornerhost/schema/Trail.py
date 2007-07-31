
from strongbox import *
from pytypes import DateTime

class Trail(Strongbox):
    ID = attr(long)
    user = attr(str)
    what = attr(str)
    tstamp = attr(DateTime, default="now")
    server = attr(str)
    note = attr(str)
