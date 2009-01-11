from shared import *
import duckbill
import zebra
from decimal import Decimal
cur = SQL.cursor()

# finally, I get to apply the crosstab story!
# ( http://www.devshed.com/Server_Side/MySQL/MySQLWiz/ )

cur.execute(
    """
    SELECT DATE_FORMAT(bs.opened,'%m/%Y') x,
           SUM(IF(bs.cycLen='month',rate,0)) AS new_monthly,
           SUM(IF(bs.cycLen='year',rate,0)) AS new_yearly
    FROM bill_subscription bs, bill_account ba
    WHERE bs.accountID = ba.ID AND ba.status != 'closed'
    GROUP BY x
    ORDER BY bs.opened
    """)

## display the chart ########################

print >> RES, zebra.fetch("dsp_head", {"errors":[]})

print >> RES, "<h2>sales</h2>"
print >> RES, "<p><i>(Sum of new monthly/yearly subscriptions per month)</i><br>"
print >> RES, "base = monthly charges, renew = yearly renewals"
print >> RES, '</p>'

print >> RES, '<table  cellspacing="0" cellpadding="2" width="500">'
print >> RES, '<tr><th align="left">period</th>'
print >> RES, '<th align="right">new/mo</th>'
print >> RES, '<th align="right">new/yr</th>'
print >> RES, '<td>&nbsp;</td>'
print >> RES, '<th align="right">base</th>'
print >> RES, '<th align="right">renew</th>'
print >> RES, '<th align="right">total</th>'
print >> RES, '</tr>'

this, next = "odd", "even"
totM, totY = 0, 0
renewals = [0] * 12; periodnum = 0

for row in cur.fetchall():
    period = row[0]
    monthly = Decimal(row[1])
    yearly = Decimal(row[2])
    base = totM

    renew = renewals[periodnum % 12]
    renewals[periodnum % 12] += yearly
    periodnum +=1

    totP = monthly + yearly + base + renew

    
    print >> RES, '<tr class="%s">' % this
    print >> RES, '<td>%s</td><td align="right">%s</td><td align="right">%s</td>' \
          % (period, monthly, yearly)
    print >> RES, '<td>&nbsp;</td><td align="right">%s</td><td align="right">%s</td>' \
          % (base, renew)
    print >> RES, '<td align="right" style="background:white">%s</td>' % totP
    print >> RES, '</tr>'

    totM += monthly
    totY += yearly
    this, next = next, this


print >> RES, '<tr><td align="right"><b>grand total:</b></td>'
print >> RES, '<td align="right"><b>%s</b></td>' % totM
print >> RES, '<td align="right"><b>%s</b></td>' % totY
print >> RES, "</tr></table>"

print >> RES, "<br>&nbsp;<br>"

print >> RES, "<b>NOTE:</b> this page does NOT include cancelled accounts,<br> "
print >> RES, "even if the customer paid for certain months. Therefore, sales for some<br> "
print >> RES, "may have been slightly higher than the numbers shown here."
