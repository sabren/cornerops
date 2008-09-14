
## public version of user.app  #################################
from cornerhost import UserApp, UserClerk
from cornerhost.tiles import makeUserWebMap, GenshiTile
from weblib import Finished, Redirect

app = UserApp(USER, CLERK, sess=SESS)
app.default="list_sites"
app.isAdmin=False
try:
    app.dispatch(req=REQ, res=RES)
except (AssertionError, Redirect, Finished):
    raise
except:
    handleError("An unknown error occurred.", USER)
