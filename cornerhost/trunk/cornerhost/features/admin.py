from strongbox import BoxView
from handy import readable, trim
from panel import ControlPanelFeature
from cornerhost.grunts import UserClerk
from cornerhost import User, Domain, Server, Signup, Plan
from cornerhost import remote
from platonic import Model
from weblib import Redirect
from pytypes import Date


## admin only ####################################
  
class AdminFeature(ControlPanelFeature):
    def __init__(self, clerk):
        self.user = None
        self.clerk = clerk


## screens #######################################
        
class ServerScreen(AdminFeature):
    def invoke(self, _clerk):
        return Model(servers=[
            BoxView(s) for s in _clerk.match(Server, status="active")])


class ListSignups(AdminFeature):
    def invoke(self, _clerk):
        signups = _clerk.match(Signup)
        def byDate(a,b):
            return cmp(a.TS, b.TS)
        signups.sort(byDate) 
        return Model(signups=[BoxView(p) for p in signups])

class ReviewSignup(AdminFeature):
    def invoke(self, _clerk, ID):
        p = _clerk.fetch(Signup, ID=ID)
        return Model(signup=BoxView(p))


class MakeUserCommand(AdminFeature):
    
    # this isn't exposed to the web at all, and shouldn't be!
    def makeUser(self, server, p):
        """
        create the actual user and return the password
        """
        # @TODO: move makeUser to an auto-setup script
        # @TODO: make actual user object, then reuse logic in addnew script
        assert isinstance(p, Signup)
        assert p.plan is not None, "signup didn't have a plan"
        assert p.username is not None, "didn't have a username"
        assert p.fullname is not None, "didn't have a fullname"
        res = remote.getBeaker(server).addnew(p.plan, p.username, p.fullname)
        return res.strip().split()[-1] # from "password for user is pass"

    def invoke(self, _clerk, signupID, account, plan, server, cycLen):
            
        p = _clerk.fetch(Signup, ID=long(signupID))
        p.plan = plan # @TODO: capture plan in cornerhost signups
        p.username = account
        p.cycLen = cycLen

        #try:
        pw = self.makeUser(server, p)
        #except xmlrpclib.Fault, f:
        #    print >> self, "XMLRPC fault: %s" % f.faultString
        #    return 

        ## now the account in duckbill:
        u = _clerk.fetch(User, username=account)
        u.account = p.toDuckbill()
        _clerk.store(u)

        ## @TODO: keep the signup around, marked as done?
        p.status="filled"
        _clerk.store(p)
        
        ## show the password!
        #@TODO: make this do something sensible instead
        assert 0, "password for %s is %s" % (account, pw)
        return Model(message=trim(
            '''
            <p>password for %s is %s<br/>
            <a href="admin.app?action=jump&jumpto=%s">see user</a></p>
            ''' % (account, pw, username)))


class TrafficScreen(AdminFeature):
    # this should be a GET on /users sorted by traffic
    # also on /servers for the server list
    def invoke(self, _clerk, server='%'):
        mod = Model(readable = readable)
        yesterday = Date("today")-1        
        mod["server"] = server
        cur = _clerk.storage.dbc.cursor()
        sql =\
            """
            SELECT u.username, p.name, s.name, t.traffic
            FROM sys_user u, sys_user_traffic t, sys_server s, sys_plan p
            WHERE u.ID=t.userID
              AND p.ID=u.planID
              AND s.ID=u.serverID
              AND t.whichday = '%s'
              AND s.name like '%s%%'
            ORDER BY traffic DESC
            LIMIT 20
            """ % (yesterday.toSQL(), mod["server"])
        cur.execute(sql)
        mod["each"] = [{
            "username":username,
            "plan": plan,
            "server":server,
            "traffic":traffic,
            } for username, plan, server,traffic in cur.fetchall()]

        cur.execute(
            """
            SELECT name FROM sys_server
            """)
        mod["servers"] = [{"server":row[0]} for row in cur.fetchall()]
        return mod


## commands ######################################
    
class JumpCommand(AdminFeature):
    # POST: returns Redirect
    
    def invoke(self, _clerk, _sess, jumpto=None):
        """
        action to jump to particular user
        """
        jumpto = jumpto
        assert jumpto, "no value given for jumpto"
        u = self.findUser(_clerk, jumpto)
        _sess["username"] = u.username
        raise Redirect("user.app") #@TODO: decouple this!

    def findUser(self, _clerk, jumpto):
        try:
            if "." in jumpto:
                d = _clerk.matchOne(Domain, domain=jumpto)
                u = d.user
            else:
                u = _clerk.matchOne(User, username=jumpto)
        except LookupError:
            raise AssertionError, "couldn't resolve %s" % jumpto
        return u





class GenHttpConfCommand(AdminFeature):
    # POST to /server/xyz/genhttpconf
    def invoke(self, server):
        beaker = remote.getBeaker(server)
        return Model(
            message="restarting apache on %s: %s" \
            % (server, beaker.genhttpconf()))
    



class UserSpecific(AdminFeature):
    # @TODO: pass in username explicitly
    def loadUser(self, _clerk, _sess):
        return _clerk.fetch(
            User, username=_sess["username"])



class UpdateUserCommand(UserSpecific):
    # PUT to /user/
    def invoke(self, _clerk, _sess, status, plan, diskextra, bandextra, boxextra,dbextra):
        user = self.loadUser(_clerk, _sess)
        user.status = status
        user.plan = _clerk.fetch(Plan, name=plan)
        user.diskextra = diskextra
        user.bandextra = bandextra
        user.boxextra = boxextra
        user.dbextra = dbextra
        _clerk.store(user)
        raise Redirect("user.app") #@TODO: hide the filename somehow
    


class IsPasswdCommand(UserSpecific):
    # could be GET but *is* a POST for security (logfiles)... hrm..
    def invoke(self, _clerk, _sess, password):
        if self.loadUser(_clerk, _sess).ispasswd(password):
            return Model(message="yes")
        else:
            return Model(message="no")


def reverse(string):
    chars = [c for c in string]
    chars.reverse()
    return "".join(chars)
                   
class UserDelCommand(UserSpecific):
    def invoke(self, _clerk, _sess, reversed):
        user = self.loadUser(_clerk, _sess)
        if reverse(user.username) == reversed:
            return Model(message=user.getBeaker().userdel(user.username))
        else:
            return Model(message="reversed name did not match")
