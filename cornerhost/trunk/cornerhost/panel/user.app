
## public version of user.app  #################################
from cornerhost import UserApp
from cornerhost.tiles import UserPage, makeUserWebMap, ZebraTile
from weblib import Finished, Redirect

ZebraTile.path = "../skin"
app = UserApp(USER, CLERK, sess=SESS)
app.tiles = makeUserWebMap(UserPage)
app.default="list_sites"
app.isAdmin=False
try:
    app.dispatch(req=REQ, res=RES)
except (AssertionError, Redirect, Finished):
    raise
except:
    handleError("An unknown error occurred.", USER)
