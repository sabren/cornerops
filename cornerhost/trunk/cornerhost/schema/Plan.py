from strongbox import *

class Plan(Strongbox):
    ID = attr(long)
    name = attr(str)
    bandquota = attr(long, default=0)
    diskquota = attr(long, default=0)
    boxquota = attr(long, default=0)
    dbquota = attr(long, default=0)
    monthlyCost = attr(int, default=10)

    # special operators:
    UNLIMITED = 0
    FORBIDDEN = -1

