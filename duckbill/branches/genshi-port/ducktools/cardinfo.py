#!/usr/bin/python2.5 -i
"""
usage: ./cardinfo.py account

will prompt for password and then show
the decrypted credit card information
for the account.

you can then update the card manually with:

acc.carinfo.xyz = whatever...
acc.cardinfo.encrypt()
acc = CLERK.store(acc)

"""

import getpass
import duckbill
import duckbill.config
import sys


CLERK = duckbill.config.makeClerk()

def getAccountObject(username):
    try:
        return CLERK.matchOne(duckbill.Account,  account=username)
    except LookupError:
        print "couldn't find user: %s" % username
        sys.exit()

def getUsername():
    if len(sys.argv) != 2:
        sys.exit()        
    return sys.argv[1]


def decrypt(acc):
    if acc.cardinfo.isEncrypted():
        print "found encrypted cardinfo for %s." % acc.account
        while True:
            phrase = getpass.getpass("passphrase:")
            try:
                acc.cardinfo.decrypt(phrase)
                break
            except ValueError:
                print "nope."
    else:
        print "no cardinfo for account %s" % acc.account


def getDecryptedAccount(username):
    acc = getAccountObject(username)
    decrypt(acc)
    return acc




if __name__=="__main__":

    print __doc__ 
    username = getUsername()
    acc = getDecryptedAccount(username)

    print "account:", acc.account
    print "status:", acc.status
    print "autobill:", acc.autobill
    print "owner:", acc.cardinfo.owner
    print "number:", acc.cardinfo.number
    print "lastfour:", acc.lastfour
    print "expire:", acc.cardinfo.expire


    #@TODO: touching cardinfo should make acc.isDirty=True
    acc.private.isDirty=True
