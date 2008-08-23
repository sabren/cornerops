# admin.app
from cornerhost import AdminApp, User
from cornerhost.tiles import GenshiTile
app = AdminApp(CLERK, SESS)
app.tiles.update({
    "servers"      : lambda : GenshiTile("servers.gen"),
    "signups"      : lambda : GenshiTile("signups.gen"),
    "review"       : lambda : GenshiTile("review.gen"),
    "traffic"      : lambda : GenshiTile("traffic.gen"),
    "genhttpconf"  : lambda : GenshiTile("message.gen"),
    "ispasswd"     : lambda : GenshiTile("message.gen"),
    "setup"        : lambda : GenshiTile("message.gen"),
    "userdel"      : lambda : GenshiTile("message.gen"),
})
app.defaultAction="servers"
app.isAdmin = True
app.dispatch(req=REQ, res=RES)
