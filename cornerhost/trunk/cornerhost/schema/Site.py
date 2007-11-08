__ver__="$Id: Site.py,v 1.6 2007/03/30 04:14:45 sabren Exp $"
import re
from strongbox import *
import cornerhost

class Site(Strongbox):
    ID = attr(long)
    docroot = attr(str, default='')
    logdir = attr(str)
    extra = attr(str)
    haslogs = attr(int, okay=[0,1], default=1)
    haserrs = attr(int, okay=[0,1], default=0)
    usealias = attr(int, okay=[0,1], default=1)
    domain = link(lambda : cornerhost.Domain)
    aliases = linkset((lambda : cornerhost.Domain), "site")
    user = link(lambda : cornerhost.User)
    suExec = attr(int, okay=[0,1], default=0)

    def get_docroot_prefix(self):
        return self.user.docroot

    def get_default_docroot(self):
        return '%s/%s' % (self.docroot_prefix, self.domain.domain)

    def set_docroot(self, value):
        if value:
            if value.count('..'):
                raise ValueError, "'..' not allowed in docroot"
            if not re.match(r'^(\w|\.|-|/)*$', value):
                raise ValueError, "invalid characters in docroot: %s" % value
        self.onSet('docroot', (value or '').replace("\n", ""))

    def get_docroot(self):        
        return self.private.docroot

    def get_fallbackURL(self):
        if self.domain.name.endswith(".sabren.com"):
            return "http://%s/" % self.domain.name
        else:
            return "http://%s.%s.sabren.com/" \
                   % (self.domain.name, self.user.server.shortname)
    
