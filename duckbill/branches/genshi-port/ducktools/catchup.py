#!/usr/bin/python2.5
"""
This runs the catchup routine, and sends
statements if necessary. You can run it
as often as you like, but it's probably
best to run it once every night.
"""
__ver__="$Id: nightly.py,v 1.20 2007/07/31 08:21:59 sabren Exp $"
import sys
import duckbill
from handy import trim, sendmail
from handy import daysInLastMonth
from pytypes import Date
from storage import where

try:
    #@TODO: clean up this hack (open source sanitation)
    from taskconfig import FROM
except:
    FROM = "somebody@example.com"



#@TODO: Statement ought to be an object backed by test cases.

def makeStatement(acc):
    """
    generate a statement for the person....
    """
    total = 0
    stmt=""
    name = (acc.fname + " " + acc.lname).strip()
    stmt += "\n"
    stmt += "Account: " + acc.account + "\n"
    stmt += "-" * 70 + "\n"
    es = acc.events
    es.sort()
    for e in es:
        if e.posted > Date("today"):
            continue # allow future posting of charges (eg, lifetime account)
        stmt += "%s  %-50s%8s\n" % (e.posted.toDate().toUS(), e.note, e.value)
        total += e.value
    stmt += ("-" * 70) + "\n"
    stmt += "%70s\n" % ("total: " +str(total))
    return (acc.fname, name, acc.email, stmt, total)


def sendStatement(acc):
    fromAddr = FROM
    fname, name, email, stmt, grand = makeStatement(acc)
    #if acc.company:
    #    fname = acc.company
    pastDue = acc.amountPastDue(lastDue)
    brand = acc.brand.title().replace('Dcd', 'DCD')
    if brand == 'DCD hosting': pastDue = None # TODO: fix this!
    header =[trim(
        """
        From: %(fromAddr)s
        To: %(name)s <%(email)s>
        """ % locals())]
    if acc.email2:
        header.append("CC: %s\n" % acc.email2)
    header.append(trim(
        """
        Subject: %(brand)s statement [$%(grand)s]
        """ % locals()))
    header = "".join(header)

    if grand <= 0:
        grand_msg = "You owe nothing at this time.\n"
    else:
        if pastDue:
            grand_msg = trim(
                """
                Amount Due: $%s.

                ** NOTE: YOUR ACCOUNT IS PAST DUE.
                ** PLEASE PAY YOUR BILL IMMEDIATELY.

                """ % (grand))
        elif acc.autobill and acc.lastfour:
            grand_msg = trim(
                """
                Amount Due: $%s.

                This amount will be charged to your credit
                card after 48 hours. The card we have on
                file for you ends with %s.

                """) % (grand, acc.lastfour)
        else:
            grand_msg = trim(
                """
                Amount Due: $%s.

                Please pay this amount by %s.

                """)  % (grand, nextDue)

        ## now cap it off:
        brand = acc.brand
        if brand == 'DCD hosting': brand='cornerhost'
        grand_msg += trim(
            """
            You may pay via credit card, PayPal, check
            or money order. For details, visit:

                http://www.%s.com/payment/

            Remember, you can pay by the month *or* by the
            year. If you would like to change your billing
            cycle, just drop me a note when you pay your bill.
            """ % brand)


    #@TODO: strip out my name. get this whole thing into genshi or something.
    msg = trim(
        """
        =============================================================

        Hello %s,

        This is your statement for %s.

        %s
        Thanks!

        Michal J Wallace
        http://www.%s.com/

        =============================================================
        """) % (fname, acc.brand, grand_msg, acc.brand.replace(' ',''))


    if (grand <= 0) and acc.statementStrategy=="ifBalance":
        print "no statement sent for %s (%s) : no balance due" % (name, acc.account)
    else:
        print "sending statement for %s (%s): $%s" % (name, acc.account, grand)
        sys.stdout.flush()
        #print header + msg + stmt
        sendmail(header + msg + stmt)




if __name__=="__main__":

    CLERK = duckbill.config.makeClerk()

    today = Date("today")
    lastDue = today - daysInLastMonth() + 15
    nextDue = today + 15

    dueAccounts = []

    for acc in CLERK.match(duckbill.Account, where("status") != "closed"):
        #@TODO: can I do multiple where clauses?
        if acc.status=="comped": continue
        
        ## @TODO: call postCharges() but figure out how to trap errors [??]

        for sub in acc.subscriptions:
            try:
                sub.catchup()
                CLERK.store(acc) # not sub, because of bug...
            except Exception, e:
                print "ERROR [%s>%s]:" % (acc.account, sub.username), str(e)


        if acc.isDue():
            dueAccounts.append(acc)
            acc.catchup()
            sendStatement(acc)
            # only store changes once bill is sent:
            CLERK.store(acc)
