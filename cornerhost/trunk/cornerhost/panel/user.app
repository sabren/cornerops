
## public version of user.app  #################################
from cornerhost import UserApp
from cornerhost.tiles import makeUserWebMap, GenshiTile
from weblib import Finished, Redirect

GenshiTile.path = "../skin"
app = UserApp(USER, CLERK, sess=SESS)
app.tiles = makeUserWebMap()
app.default="list_sites"
app.isAdmin=False
try:
    app.dispatch(req=REQ, res=RES)
except (AssertionError, Redirect, Finished):
    raise
except:
    handleError("An unknown error occurred.", USER)
