from cornerhost import remote
import cornerhost
from strongbox import *
from pytypes import DateTime
from decimal import Decimal

mx, datetime = None, None
try:    
    import datetime    
except ImportError:
    pass
try:
    import mx
except:
    pass
    

class Server(Strongbox):
    ID = attr(long)
    name = attr(str, default="")
    shortname = attr(str)
    ipaddress = attr(str)
    load1 = attr(Decimal)
    load5 = attr(Decimal)
    load15= attr(Decimal)
    stamp = attr(DateTime)
    space = attr(str)
    memory = attr(str)
    uptime = attr(str)
    users = linkset((lambda : cornerhost.User), "server")
    
    def getBeaker(self):
        assert self.name
        return remote.getBeaker(self.name)

    def getMySQL(self):
        assert self.name
        return remote.getMySQL(self.name)

    def get_age(self):
        # return age in minutes since last beaker checkin
        assert datetime or mx, "need real datetime module to call get_age!"
        if datetime:
            delta = datetime.datetime.now() - self.stamp.to_datetime()
            # UGH! you get a tuple of days, seconds.
            secs_in_day = 3600*24
            secs_in_min = 60
            return ((delta.days * secs_in_day) + delta.seconds) / secs_in_min
        else:
            return int((mx.DateTime.now() - self.stamp.toMx()).minutes)
