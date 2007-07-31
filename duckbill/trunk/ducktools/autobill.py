#!/usr/bin/python2.5
"""

"""
import sys, handy
import operator
import getpass
import pprint
import duckbill
import optparse
from duckbill import Event, Account, Receivables
from pytypes import Date, DateTime


try:
    #@TODO: clean up this hack (open source sanitation)
    from taskconfig import FROM
except:
    FROM = "somebody@example.com"


TWO_DAYS_AGO=Date("today")-2

# * sum: should be in handy
def sum(amounts):
    return reduce(operator.add, [0]+ amounts)

# * get accounts to bill 
def getAccountsToBill(r):
    return [a for a in r.dueAccounts()
            if (a.autobill and
                a.balance() > 0 and
                (a.amountPastDue(TWO_DAYS_AGO) > 0))]


# * email customer
def emailCustomer(acc, result, details, lastfour, amount):
    model = {}
    model["email"] = acc.email
    model["fname"] = acc.fname
    model["brand"] = acc.brand
    model["account"] = acc.account
    model["lastfour"] = lastfour
    model["amount"] = amount
    model["result"] = result
    model["details"] = details
    model["signature"] = open("/home/sei/.signature").read()

    model['fromAddr'] = FROM
    message = handy.trim(
        """
        From: %(fromAddr)s
        To: %(email)s
        BCC: %(fromAddr)s
        Subject: credit card denied

        Hi %(fname)s,

        Your %(brand)s account (username %(account)s)
        is set up for automatic billing, and my system
        just attempted to post a charge of $%(amount)s
        to your credit card - the one with the number
        ending in %(lastfour)s. The bank responded
        with the following error:

            %(result)s
            %(details)s


        Could you please look into this? If you would like
        to use a different means of payment or enter a
        different card, you can do so here:

            http://%(brand)s.com/payment/

        Thanks!

        %(signature)s
        """) % model

    action = "e"
    while 1:
        if action=="e":
            message=handy.edit(message)
        elif action=="s":
            handy.sendmail(message)
            break
        elif action=="a":
            break
        action = raw_input("[e]dit, [a]bandon, [s]end? ")


# * parseCommandLine
def parseCommandLine():
    op = optparse.OptionParser()
    op.add_option("--batch", dest="batch",
                  action="store_true", default=False,
                  help="batch mode (no prompting for feedback)")
    op.add_option("--notify", dest="notify",
                  action="store_true", default=False,
                  help="send list and then exit")
    (opts, args) = op.parse_args()
    return opts, args

# * main routine
def main():
    opts, args = parseCommandLine()
    
    clerk = duckbill.config.makeClerk()
    dbc = clerk.storage.dbc
    
    accts = getAccountsToBill(Receivables(dbc, clerk))
    #accts = clerk.match(Account, account="ftempy")
    total = sum([a.balance() for a in accts])
    count = len(accts)

    if count == 0:
        sys.exit()


    if opts.notify:
        detail = "\n".join(["    %s : %s" % (a.account, a.balance())
                            for a in accts])
        handy.sendmail(handy.trim(
            """
            To: %s
            From: %s
            Subject: time to run cards
            
            you have %s account(s), worth %s ready for autobill

            %s
            """) % (FROM, FROM, count, total, detail))
    else:
        # get passphrase and decrypt the cards:
        while True:
            phrase = getpass.getpass("passphrase: ")
            try:
                for acc in accts:
                    #print acc.account,
                    #print acc.cardinfo.isEncrypted()
                    acc.cardinfo.decrypt(phrase)
                break
            except ValueError, e:
                if str(e).count("I/O operation on closed file"):
                    print "nope"
                else:
                    raise

        ## @TODO: this has to come after gpg stuff because otherwise
        ## duckpag changes os.environ["GNUPG"] -- but WHY?!?!
        import os
        tmp = os.environ.get("GNUPGHOME")
        import duckpay
        if tmp:
            os.environ["GNUPGHOME"] = tmp
        else:
            del os.environ["GNUPGHOME"]


        ## @TODO: clean this mess up!! #########################
        sys.path.insert(0, "/home/sei/lib/ensemble")
        import ensemble
        perl=ensemble.Director("/home/sei/lib/ensemble/ensemble.pl")
        perl.loadModule("CyberSourceAuth", "cybs")
        assert perl.cybs.okay(), "didn't load okay"
        ########################################################

        import reasons

        # now charge them:        
        for acc in accts:

            amount = acc.balance()
            if amount == 0: continue
            print "%s ($%s):" % (acc.account, amount),
            sys.stdout.flush()
            if not opts.batch:
                if raw_input("[yes|no]").lower() not in ["y","yes"]:
                    continue
                    
            
            # this is basically stolen from process.cgi:            
            if  " " not in acc.cardinfo.owner:
                print "bad card owner: %s" % acc.cardinfo.owner
                owner = raw_input("enter new name: ")
                if not owner.strip():
                    print "skipping..."
                else:
                    acc.cardinfo.owner = owner.strip()
                    acc.cardinfo.encrypt()
                    #@TODO: touching cardinfo should make acc.isDirty=True
                    acc.private.isDirty=True
                    clerk.store(acc)
                    print "updated...",
                print "will try again next time"
                continue
                    
                    
            fname, lname = acc.cardinfo.owner.split(" ", 1)
            orderid = handy.uid()
            request = {
                "ccAuthService_run":       "true",
                "merchantReferenceCode":   orderid,
                "billTo_firstName":        fname,
                "billTo_lastName"  :       lname,
                "card_expirationMonth":    acc.cardinfo.expire.m,
                "card_expirationYear":     acc.cardinfo.expire.y,
                "billTo_street1":          acc.address1,
                "billTo_city":             acc.city,
                "billTo_state":            acc.state,
                "billTo_postalCode":       acc.postal,
                "billTo_country":          acc.countryCD,
                "billTo_email":            acc.email,
                "card_accountNumber":      acc.cardinfo.number,
                "sei_userid":              acc.account,
                "purchaseTotals_currency": "USD",
                "purchaseTotals_grandTotalAmount": str(amount),
            }

            # do it:
            status, reply = perl.cybs.auth(request)

            if status!=0:
                print "SYSTEM ERROR"
                pprint.pprint(reply)
                
            elif reply["decision"] in ["ERROR","REJECT"]:
                pprint.pprint(request)
                pprint.pprint(reply)
                reason = str(reasons.code[int(reply["reasonCode"])][0])
                print "###", reason, "#####"
                if opts.batch: continue
                if raw_input("send email? ").lower() in ("y", "yes"):
                    emailCustomer(
                        acc,
                        reply["decision"],
                        (  reason + "\n" + pprint.pformat(reply)),
                        acc.cardinfo.number[-4:],
                        amount)
            else:
                print reply["decision"], amount, orderid
                duckpay.post("bofa", acc.account, amount, orderid,
                             note="autopayment - thank you!")
                
# * run it 
if __name__=="__main__":
    main()
    
