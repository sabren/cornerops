#!/bin/python
"""
copycard user1 user2
"""
import cardinfo
import sys

uname1, uname2 = sys.argv[1:]

user1 = cardinfo.getDecryptedAccount(uname1)
user2 = cardinfo.getAccountObject(uname2)

for attr in ("owner", "number", "expire"):
    setattr(user2.cardinfo, attr, getattr(user1.cardinfo, attr))

user2.lastfour = user1.lastfour
user2.autobill = True

cardinfo.CLERK.store(user2)
