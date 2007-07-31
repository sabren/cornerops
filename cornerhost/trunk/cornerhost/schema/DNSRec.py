__ver__="$Id: DNSRec.py,v 1.3 2006/07/02 05:33:08 sabren Exp $"
from strongbox import *
import cornerhost
import re

class DNSRec(Strongbox):
    ID = attr(long)
    domain = link(lambda : cornerhost.Domain)
    rectype = attr(str, okay=["TXT","MX"], default="MX")
    priority = attr(int)
    value = attr(str, allowNone=False) #@TODO: validate that it's a hostname

    def get_value(self):
        """
        make sure value always has quotes for TXT records
        """
        # @TODO: this should really be a subclass
        value = self.private.value.strip().replace('\n',' ')
        if self.rectype=='TXT':
            if not value.startswith('"'): value = '"' + value
            if not value.endswith('"'): value = value + '"'
        return value
