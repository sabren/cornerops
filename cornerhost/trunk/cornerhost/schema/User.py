__ver__="$Id: User.py,v 1.11 2007/04/16 15:45:56 sabren Exp $"
from strongbox import *
from cornerhost.schema import Server,Site,Domain,Mailbox,Usage,Plan,Database
from duckbill import Account
import handy

class User(Strongbox):
    ID = attr(long)
    username = attr(str)
    diskusing = attr(long, default=0)
    diskextra = attr(long, default=0)
    bandextra = attr(long, default=0)
    boxextra = attr(long, default=0)
    dbextra = attr(long, default=0)
    bandrule = attr(str, okay=["charge","disable"], default="charge")
    status = attr(str, okay=['active','locked','closed'], default='active')

    plan = link(Plan)
    server = link(Server)
    account = link(Account)

    sites = linkset(Site, "user")
    usage = linkset(Usage, "user")
    boxes = linkset(Mailbox, "user")
    domains = linkset(Domain, "user")
    dbs = linkset(Database, "user")
   
    def getBeaker(self):
        assert self.server, "can't get beaker because user.server is None"
        return self.server.getBeaker()

    def getMySQL(self):
        assert self.server, "can't get MySQL because user.server is None"
        return self.server.getMySQL()

    def ispasswd(self, passwd):
        return self.getBeaker().ispasswd(self.username, passwd)

    def domainNames(self, onlyZones=True):
        if onlyZones:
            names=[d.domain for d in self.domains if not d.zone]
        else:
            names=[d.domain for d in self.domains]
        names.sort()
        return names

    def get_diskquota(self):
        return self.plan.diskquota + self.diskextra

    def get_bandquota(self):
        return self.plan.bandquota + self.bandextra

    def get_boxquota(self):
        return self.plan.boxquota + self.boxextra

    def set_boxquota(self,value):
        
        pass
    def set_dbquota(self,value):
        pass

    def get_dbquota(self):
        return self.plan.dbquota + self.dbextra
   
    def get_docroot(self):
        if self.plan.name=='basic':
            return '/web/simple/%s' % self.username
        else:
            return '/web/script/%s' % self.username

    def trafficUsed(self, period):
        return handy.sum([
            u.traffic
            for u in self.usage
            if u.whichday in period
        ])

    def new_mailbox(self):
        return Mailbox(user=self)

