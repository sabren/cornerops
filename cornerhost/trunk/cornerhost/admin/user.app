
## admin version of user.app #################################
from cornerhost import User, UserApp
from cornerhost.tiles import GenshiTile, makeUserWebMap
from cornerhost.features import site, admin

assert SESS.get("username"), "no user in session"
USER = CLERK.fetch(User, username=SESS["username"])

# build it:
GenshiTile.path = "../skin"
app = UserApp(USER, CLERK, SESS, isAdmin=True)
app.featureSet['save_site'] = site.AdminSaveSiteCommand
app.tiles=makeUserWebMap()
app.default='list_sites'

# run it:
app.dispatch(req=REQ, res=RES)
