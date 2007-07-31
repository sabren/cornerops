import sqlCornerhost
import zebra
import base64, zlib
import sixthday
import string
from cornerhost.schema import User

def sanitize(str):
    okay = string.digits + string.letters + "_"
    for ch in str:
        if ch not in okay:
            raise TypeError
    return str


class BeakerAuth(sixthday.Auth):
    def __init__(self, res, sess, clerk):
        self._sess = sess
        self.RES = res
        self.clerk = clerk

    def getBeaker(self, user=None):
        """
        Connect to whatever xml-rpc server the user's account is on.
        """
        usr = user or getattr(self,"key",None)
        if not usr:
            return None

        try: usr = sanitize(usr)
        except: return None

        match = self.clerk.match(User, username=usr)
        if not match:
            return None

        uobj = match[0]
        return uobj.getBeaker()
        

    def prompt (self, message, action, hidden):
        wargs = {"message": message,
                 "action": action,
                 "hidden": hidden}
        print >> self.RES, zebra.fetch("login.zb", wargs)


    def validate(self, dict):
        """
        logs in using system password, *if* the user is
        valid (has a logfile directory)
        """
        authKey = None
        u = dict.get("username")
        #return u # @TODO: ** AUTHENTICATION IS TURNED OFF!!! **
        p = dict.get("password")
        self.beaker = self.getBeaker(u)
        if self.beaker is not None:
            if self.beaker.ispasswd(u,p):
                authKey = u
        return authKey

