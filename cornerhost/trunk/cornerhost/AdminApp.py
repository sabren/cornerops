from cornerhost import Plan, User
from cornerhost.UserApp import CornerApp
from cornerhost.features.admin import *

class AdminApp(CornerApp):
    
    def __init__(self, clerk, sess):
        self.user = User(username="(admin)", plan=Plan(name="basic"))
        super(AdminApp, self).__init__(UserClerk(self.user, clerk))
        self.tiles = {}
        self.sess = sess
        self.featureSet={}
        self.featureSet["servers"] = ServerScreen
        self.featureSet["jump"] = JumpCommand
        self.featureSet["signups"] = ListSignups
        self.featureSet["review"] = ReviewSignup
        self.featureSet["make_user"] = MakeUserCommand
        self.featureSet["traffic"] = TrafficScreen
        self.featureSet["genhttpconf"] = GenHttpConfCommand
        self.featureSet["ispasswd"] = IsPasswdCommand
        self.featureSet["update_user"] = UpdateUserCommand
        self.featureSet["userdel"] = UserDelCommand

    #@TODO: this was also stolen from UserApp :/
    def prepareModel(self, req):
        model = {}
        model["error"] = None
        model["admin"] = self.isAdmin
        model["user"] = self.user
        model["changed"] = req.get("changed", None)
        model["jumpto"] = None
        return model
