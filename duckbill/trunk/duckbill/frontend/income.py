from shared import *
import duckbill
import zebra
import time
from pytypes import Date
cur = SQL.cursor()

month = time.strftime("%Y-%m")
mGoal = 6000
dGoal = mGoal / Date("today").daysInMonth()

cur.execute(
    """
    SELECT date_format(posted, '%%m-%%d') AS day, sum(amount)
    FROM   bill_event
    WHERE  posted LIKE '%s%%'
      AND  event='payment'
    GROUP BY day DESC
    """ % month)

dData = [(day, income, income-dGoal) for day, income in cur.fetchall()]


cur.execute(
    """
    SELECT date_format(posted, '%%Y-%%m') as month,
           sum(amount) as income,
           sum(amount)-%s as diff
    FROM bill_event
    WHERE  event='payment'
    GROUP BY month DESC
    """ % mGoal)
mData = cur.fetchall()


def color(amount):
    if amount == 0:
        return "black"
    elif amount < 0:
        return "red"
    else:
        return "green"



sum = lambda series: reduce((lambda a,b: a+b), series, 0)

offGoal =  sum([x[2] for x in dData])
totalIncome = sum([x[1] for x in dData])


## display the chart ########################

print >> RES, zebra.fetch("dsp_head", {"errors":[]})

print >> RES, "<h2>income for %s</h2>" % month

print >> RES, '<table style="border: solid black 1px; margin-bottom: 20px; width: 275px">'
print >> RES, "<tr><td>total income so far</td>"
print >> RES, "<td align='right'><strong>%9.2f</strong></td></tr>" % totalIncome
print >> RES, "<tr><td>monthly goal</td>"
print >> RES, "<td align='right'><strong>%9.2f</strong></td></tr>" % mGoal
print >> RES, "<tr><td>difference vs goal so far</td>"
print >> RES, "<td align='right'><strong style='color: %s'>%.2f</strong></td></tr>" % (color(offGoal), offGoal)
print >> RES, "</table>"

print >> RES, '<table  cellspacing="0" cellpadding="2" width="200px" style="float:left">'
print >> RES, '<tr><th align="left">day</th>'
print >> RES, '<th align="right">income</th>'
print >> RES, '<th align="right">diff</th>'
print >> RES, '</tr>'

this, next = "odd", "even"

for day, income, vsGoal in dData:
    
    print >> RES, '<tr class="%s">' % this
    print >> RES, ('<td>%s</td><td align="right">%.2f</td>' %
                   (day, income))

    print >> RES, '<td style="color:%s; background: #eee; text-align:right">%.2f</td>' \
          % (color(vsGoal), vsGoal)
    print >> RES, '</tr>'

    this, next = next, this

print >> RES, "</table>"


## month table:

print >> RES, "<table style='margin-left: 100px'>"
print >> RES, "<tr><th>month</th><th>income</th><th>diff</th></tr>"
for month, income, diff in mData[1:13]:
    graph = "|" * (min(100, int(income/mGoal * 100))-50)
    print >> RES, "<tr><td>%s</td><td style='text-align: right'>%.2f</td><td style='color:%s; text-align:right'>%.2f</td><td>%s</td></tr>" \
          % (month, income, color(diff), diff, graph)
print >> RES, "</table>"
