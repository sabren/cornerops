#!/usr/bin/python2.5
from duckbill import *
import duckbill.config
from pytypes import Date
import sys

CLERK = duckbill.config.makeClerk()

try:
    cutoff = Date(sys.argv[1])
except:
    print "usage: unearned.py DATE|today"
    sys.exit()

# cache the data:
subs = CLERK.match(Subscription)
evts = CLERK.match(Event)
print "cached."

sum = 0
for a in CLERK.match(Account):
    sum += a.unearnedIncome(cutoff)

print "unearned income on %s was %s" % (cutoff.toUS(), sum)
