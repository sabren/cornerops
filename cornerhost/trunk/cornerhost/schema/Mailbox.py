__ver__="$Id: Mailbox.py,v 1.6 2007/04/20 09:31:00 sabren Exp $"
from strongbox import *
import cornerhost

class Mailbox(Strongbox):
    ID = attr(long)
    mailbox = attr(str, okay="^pop_[a-z0-9_]+$", allowNone=False)
    user = link(lambda : cornerhost.User)

    def get_rules(self):
        res = []
        doms = self.user.domains
        for d in self.user.domains:
            if d.mailto == self.mailbox:
                res.append(d.catchall)
            for r in d.rules:
                if r.mailto == self.mailbox:
                    res.append(r)
        return res
