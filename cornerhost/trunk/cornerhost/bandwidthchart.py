"""
a routine to show a bandwidth chart
"""

import string
from pytypes import Date
from handy import readable
from LimitChart import LimitChart
import sping.PIL as pid
from sixthday import App
from cornerhost import User

def showchart(REQ, RES, CLERK):

    ## find the user's bandwidth plan
    assert REQ.has_key("username")
    username = REQ["username"]


    uobj = CLERK.fetch(User, username=username)
    limit = uobj.bandquota
    assert limit!=0, "bandquota should never be zero" # divide by 0 = bad

    ## create a list of the past 30 days
    last30days = []
    day = Date("today")
    for i in range(30):
        day -= 1
        last30days.append(day.toSQL())
    last30days.reverse()


    ## fetch last 30 entries
    ## (hopefully last 30 days, but some days could be missing)
    cur = CLERK.storage.dbc.cursor() #@TODO: fix this!!
    cur.execute(
        """
        SELECT t.whichday, t.traffic
        FROM sys_user u, sys_user_traffic t
        WHERE u.ID=t.userID
          AND u.username='%s'
        ORDER BY t.whichday DESC
        LIMIT 30
        """ % username)
    hash = {}
    for (rawdate, traffic) in cur.fetchall():
        date = Date(rawdate).toSQL()
        hash[date] = traffic


    ## now get our actual 30 days, possibly with gaps:
    data = []
    for day in last30days:
        if hash.has_key(day):
            data.append(hash[day])
        else:
            data.append(None)

    # show the image:
    RES.contentType="image/png"
    chart = pid.PILCanvas(size=(250,100))
    LimitChart(250,100, limit, data).draw(chart)
    chart.save(file=RES, format="png")

