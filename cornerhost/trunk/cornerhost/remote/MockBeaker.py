import xmlrpclib
import cornerhost.remote

class MockBeaker(object):
    log = []
    crontab = ""

    def makeSiteDirs(self, username, domain):
        self.log.append("makeSiteDirs('%s','%s') " % (username, domain))

    def genmailconf(self):
        pass

    def addnew(self, plan, user):
        pass

    def addpop(self, mailbox):
        return cornerhost.remote.MOCKPASSWD

    def mqsend(self, message):
        pass
    
    def genhttpconf(self):
        pass

    def ispasswd(self, user, passwd):
        if passwd == "fail":
            return False
        else:
            return True

    def setpasswd(self, user, old, new):
        if old == "fail":
            raise xmlrpclib.Fault("?", "NO: mock setpasswd failure")
        else:
            return "ok"


    def setboxpasswd(self, box, new):
        if new == "fail":
            raise xmlrpclib.Fault("?", "NO: mock setboxpasswd failure")
        else:
            return "ok"
    

    def getcron(self, user):
        return "mock crontab for %s" % user

    def setcron(self, user, crontab):
        self.__class__.crontab = crontab
        if crontab.startswith("test"): return ""
        return "mock setcron result"
