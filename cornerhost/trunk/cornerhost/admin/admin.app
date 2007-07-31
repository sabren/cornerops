# admin.app
from cornerhost import AdminApp, User
from cornerhost import tiles
from cornerhost.tiles import AdminUserPage, ZebraTile, SimpleTile
ZebraTile.path = "../skin"
app = AdminApp(CLERK, SESS)
app.tiles = tiles.makeUserWebMap(AdminUserPage)
app.tiles.update({
    "servers"      : lambda : AdminUserPage(ZebraTile("servers.zb")),
    "signups"      : lambda : AdminUserPage(ZebraTile("signups.zb")),
    "review"       : lambda : AdminUserPage(ZebraTile("review.zb")),
    "traffic"      : lambda : AdminUserPage(ZebraTile("traffic.zb")),
    "genhttpconf"  : lambda : AdminUserPage(ZebraTile("message.zb")),
    "ispasswd"     : lambda : AdminUserPage(ZebraTile("message.zb")),
    "setup"        : lambda : AdminUserPage(ZebraTile("message.zb")),
    "userdel"      : lambda : AdminUserPage(ZebraTile("message.zb")),    
})
app.defaultAction="servers"
app.isAdmin = True
app.dispatch(req=REQ, res=RES)
