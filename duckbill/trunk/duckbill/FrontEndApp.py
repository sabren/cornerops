"""
Front end for duckbill
"""
from __future__ import with_statement
__ver__="$Id: FrontEndApp.py,v 1.30 2007/03/30 00:35:53 sabren Exp $"

import duckbill
import sixthday
import zebra
import weblib
from duckbill import Account, Event, Subscription
from contextlib import contextmanager



class FrontEndApp(sixthday.AdminApp):

    def act_(self):
        self.create_account()

    def jumpto_accounts(self, accounts, searchOnly):
        if len(accounts) == 0:
            raise IndexError("not found")
        elif len(accounts) == 1 and not searchOnly:
            self.input["ID"] = accounts[0].ID
            self.show_account()
        else:
            self.write("<h1>search results:</h1>")
            self.write("<ul>")
            for a in accounts:
                self.write('<li><a href="index.py?action=jump&jumpto=')
                self.write(a.account)
                self.write('">')
                self.write('%s (%s)' % (a.account, a.status))
                self.write('</a></li>')
            self.write("<ul>")


    def act_jump(self):
        if self.input.get("jumpto"):
            jump = self.input["jumpto"]
            try:
                if jump.startswith("#"):
                    self.input["ID"]=self.clerk.match(Event,
                                                      refnum=jump[1:])[0].ID
                    self.edit_event()
                    

                elif jump.count(" "):
                    fn, ln = jump.split(" ", 1)
                    kw = {}
                    if fn != "*": kw['fname']=fn
                    if ln != "*": kw['lname']=ln
                    res = self.clerk.match(Account, **kw)
                elif jump.count("@"):
                    res = self.clerk.match(Account, email=jump)
                else:
                    res = self.clerk.match(Account, account=jump)
                    
                if not res:
                    subs = self.clerk.match(Subscription, username=jump)
                    res = [s.account for s in subs]

                if res:
                    self.jumpto_accounts(res, self.input.has_key('searchOnly'))
                else:
                    self.write("%s sub/acct not found" % jump)
                        
            except IndexError:
                self.write("%s not found" % jump)
                
                
        else:
            self.write("no value given for jump")
       

    def requireAccountID(self):
        assert self.model.get("accountID"), "no accountID given"


    ### accounts ############################################

    def show_account(self):
        self.generic_show(Account, "sho_account")

    def edit_account(self):
        self.generic_show(Account, "frm_account")

    def create_account(self):
        self.generic_create(Account, "frm_account")

    def save_account(self):
        acct = self.generic_save(Account)
        self.redirect("index.py?action=show&what=account&ID=%i"
                      % int(acct.ID))

    @contextmanager
    def accountUpdate(self, paramName="accountID"):
        try:
            assert self.input.get(paramName), "give me an accountID"
            acc = self.clerk.fetch(Account, ID=int(self.input[paramName]))
            yield acc
        except:
            raise
        else:
            acc = self.clerk.store(acc)
            self.redirect("index.py?action=show&what=account&ID=%i"
                          % int(acc.ID))

    def act_close_account(self):
        assert self.input.get("reason"), "give me a reason"
        with self.accountUpdate(paramName='ID') as acc:
            acc.close(self.input["reason"])
            assert acc.status == 'closed', "??!"

    def act_catchup(self):
        with self.accountUpdate() as acc:
            acc.postCharges()

    def act_stop_autobill(self):
        with self.accountUpdate() as acc:
            acc.postCharges()
            acc.lastfour=''
            acc.cardinfo=None
            acc.autobill=False

    def act_grace(self):
        with self.accountUpdate() as acc:
            acc.grace(why=self.input['note'], untilWhen=self.input['expires'])


    ### subscriptions ############################################


    def create_subscription(self):
        self.requireAccountID()
        self.generic_create(Subscription, "frm_subscription")

    def edit_subscription(self):
        self.generic_show(Subscription, "frm_subscription")
        
    def save_subscription(self):
        if self.input.get("ID"):
            s = self.generic_save(Subscription)
        else:
            self.requireAccountID()
            a = self.clerk.fetch(Account, ID=self.model["accountID"])
            s = self._getInstance(Subscription)
            s.account = a
            s = self.clerk.store(s)
        self.redirect("index.py?action=show&what=account&ID=%i"
                      % int(s.account.ID))
        
    ### events ############################################

    def create_event(self):
        self.requireAccountID()        
        self.generic_create(Event, "frm_event")

    def edit_event(self):
        self.generic_show(Event, "frm_event")

    #@TODO: save_event and save_subscription are almost identical!
    def save_event(self):
        if self.input.get("ID"):
            e = self.generic_save(Event)
        else:
            self.requireAccountID()
            a = self.clerk.fetch(Account,ID=self.model["accountID"])
            e = self._getInstance(Event)
            e.account = a
            e = self.clerk.store(e)
        self.redirect("index.py?action=show&what=account&ID=%i"
                      % int(e.account.ID))

    def getCheckedEvents(self):
        eids = self.input.get("eventID", ())
        if type(eids) == tuple:
            ids = eids
        else:
            ids = (eids,)
        return [self.clerk.fetch(Event, ID=eid) for eid in ids]

    def jumpToAccount(self, accID):
        self.redirect("index.py?action=show&what=account&ID=%s" % accID)

    def act_void(self):
        for e in self.getCheckedEvents():
            e.event = 'void'
            e.note = "void: " + e.note
            self.clerk.store(e)
        self.jumpToAccount(self.input["accountID"])

    def die(self, msg):
        assert 0, msg # @TODO: fix this

    def fetchAccount(self, account):
        try:
            return self.clerk.fetch(Account, account=account)
        except LookupError:
            self.die("couldn't find destination account")        

    def act_move_events(self):
        acc = self.fetchAccount(self.input["dest_account"])
        for e in self.getCheckedEvents():
            acc.events << e
        self.clerk.store(acc)
        self.jumpToAccount(acc.ID)
