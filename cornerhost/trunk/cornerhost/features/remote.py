# remote features
from panel import ControlPanelFeature, extractNewPass
from platonic import Intercept
from cornerhost import Database, safety

import xmlrpclib, socket
import base64, zlib

## mysql commands #################################

class MySQLFeature(ControlPanelFeature):
    pass

class CreateDatabaseCommand(MySQLFeature):
    def invoke(self, _user, _clerk, dbname):
        try:
            _user.getMySQL().createDatabase(_user.username, dbname)
        except ValueError, e:
            raise Intercept(str(e))
        _user.dbs << Database(dbname=dbname)
        _clerk.store(_user)
        
class DropDatabaseCommand(MySQLFeature):
    def invoke(self, _user, _clerk, dbname):
        db = safety.safeDb(_user, dbname)
        _user.getMySQL().dropDatabase(_user.username, dbname)
        _clerk.delete(Database, db.ID)


class SetMySQLPasswordCommand(MySQLFeature):
    def invoke(self, _user, new1, new2):
        try:
            pwd = extractNewPass(new1,new2)
            if "'" in pwd: raise ValueError("invalid password")
        except ValueError, e:
            raise Intercept(str(e))
        _user.getMySQL().setPassword(_user.username, pwd)


## beaker commands ###############################

class SetCronCommand(ControlPanelFeature):
    def invoke(self, _user, crontab=""):
        if not crontab.endswith("\n"):
            crontab += "\n"
        error = _user.getBeaker().setcron(
            _user.username, crontab).strip()
        if error:
            if ":" in error:
                tempfilepath, line, msg = error.split(":",2)
                error = "line %s: %s" % (line, msg)
            raise Intercept(error)


class SetPasswordCommand(ControlPanelFeature):

    def invoke(self, _user, old, new1, new2):
        #@TODO: this ought to be universal or something. :/
        # it [was?] almost EXACTLY like SetBoxPasswordCommand
        try:
            _user.getBeaker().setpasswd(
                _user.username, old, extractNewPass(new1, new2))
        except xmlrpclib.Fault, f:
            raise Intercept(f.faultString)
        except socket.error, e:
            raise Intercept("socket error: %s" % e)
        except (TypeError, ValueError, LookupError, IOError), e:
            raise Intercept(self.buildErrorMessage(e))


class AnalogFeature(ControlPanelFeature):
    # note: this is handle(), not invoke()!! special case!
    def handle(self, req, res, sess):
        path = req.get("path")
        assert path, "no path given"
        try:
            ctype,content = _user.getBeaker().getContent(
                _user.username, path)
            res.addHeader("Content-Type", ctype)
            res.write(zlib.decompress(base64.decodestring(content)))
        except Exception, e:
            res.addHeader("Status", "404 Not Found")
            res.write("<h1>Not Found</h1>\n")
            res.write(str(getattr(e, "faultString", None) or e))
            res.write("<hr/>\n")
        res.end()

