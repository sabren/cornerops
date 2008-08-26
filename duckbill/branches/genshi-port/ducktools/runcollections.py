#!/usr/bin/python2.5
"""
run this nightly to warn deadbeats of their impending doom. :)
"""
import handy
import duckbill
import operator
import xmlrpclib
from pytypes import Date
import sys

clerk = duckbill.config.makeClerk()
dbc = clerk.storage.dbc

from cornerhost import User
from cornerhost import config
uclerk = config.makeClerk()

#@TODO: get rid of this completely (use duckbill.Grace instead)
# (this is just a hard-coded list)
try:
    from graced import GRACED, gracedUntil
except Exception, e:
    GRACED = []
    gracedUntil = []

for who, until in gracedUntil:
    if Date("today") <= until:
        GRACED.append(who)


try:
    PASTDUE_MAIL_TEMPLATE = open("pastdue.msg").read()
except:
    print "create a file called pastdue.msg that has your email template in it."
    sys.exit()


    
def makemail(account, email, fname, lname, total, pastdue, brand):
    cap = brand.title()
    return PASTDUE_MAIL_TEMPLATE % locals()


if __name__=="__main__":
    r = duckbill.Receivables(dbc, clerk)   
    boxes_to_restart = {}

    for acc in r.dueAccounts():
        if (acc.account in GRACED) or (acc.graced):
            continue
        
        # still here, so:
        due45, due30, due15, due0 = r.separate_ages(acc.aging())        
        pastdue = due45 + due30 + due15
        total = pastdue + due0
        if due45:

            if acc.status =='active':
                mail = makemail(acc.account, acc.email,
                                acc.fname, acc.lname,
                                total, pastdue, acc.brand)
                handy.sendmail(mail)
                acc.status = 'warned'
                acc.warned = Date("today")
                clerk.store(acc)
                print "warned account %s" % acc.account


            elif acc.status =='warned':
                if acc.warned < Date("today") - 2:
                    acc.status = 'locked'
                    clerk.store(acc)
                    print "locked account %s" % acc.account
                    try:
                        user = uclerk.match(User, username=acc.account)[0]
                        user.status='locked'
                        boxes_to_restart[user.server.name] = 1
                        uclerk.store(user)
                    except Exception, e:
                        print "couldn't lock user for locked account %s" \
                              % acc.account
                        print e

    for box in boxes_to_restart:
        beaker = xmlrpclib.ServerProxy("https://%s.sabren.com:45678/" % box)
        beaker.genhttpconf()
        
