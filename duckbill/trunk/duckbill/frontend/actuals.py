from shared import *
import duckbill
import zebra
from pytypes import FixedPoint
cur = SQL.cursor()

# finally, I get to apply the crosstab story!
# ( http://www.devshed.com/Server_Side/MySQL/MySQLWiz/ )

cur.execute(
    """
    SELECT DATE_FORMAT(e.posted,'%m/%Y') x,
           SUM(IF(e.event='charge',  amount,0)) AS charges,
           SUM(IF(e.event='payment', amount,0)) AS payments
    FROM bill_event e, bill_account ba
    WHERE e.accountID = ba.ID
    GROUP BY x
    ORDER BY e.posted
    """)

## display the chart ########################

print >> RES, zebra.fetch("dsp_head", {"errors":[]})

print >> RES, "<h2>actuals</h2>"

print >> RES, "<p><i>These are the amounts actually charged and paid.</i><br>"
print >> RES, "The total difference is LOWER than receivables, because it<br>"
print >> RES, "subtracts unearned income (people paying for multiple<br>"
print >> RES, "months or years at once).</p>"

print >> RES, '<table  cellspacing="0" cellpadding="2" width="500">'
print >> RES, '<tr><th align="left">period</th>'
print >> RES, '<th align="right">charges</th>'
print >> RES, '<th align="right">payments</th>'
print >> RES, '<th align="right">difference</th>'
print >> RES, '</tr>'

this, next = "odd", "even"
totC, totP, totD = 0, 0, 0

for row in cur.fetchall():
    period = row[0]
    charges = FixedPoint(row[1])
    payments= FixedPoint(row[2])
    diff = charges - payments

    print >> RES, '<tr class="%s">' % this
    print >> RES, '<td>%s</td><td align="right">%s</td><td align="right">%s</td>' \
          % (period, charges, payments)
    print >> RES, '<td align="right" style="background:white">%s</td>' % diff
    print >> RES, '</tr>'

    totC += charges
    totP += payments
    totD += diff
    this, next = next, this


print >> RES, '<tr><td align="right"><b>grand total:</b></td>'
print >> RES, '<td align="right"><b>%s</b></td>' % totC
print >> RES, '<td align="right"><b>%s</b></td>' % totP
print >> RES, '<td align="right"><b>%s</b></td>' % totD
print >> RES, "</tr></table>"

