## import sys
## print "content type: text/plain"
## print
## sys.stderr = sys.stdout

SITE_NAME="hydrogen duckbill"
SITE_MAIL="michal@sabren.com"

import sys
sys.path.append("/home/secure/lib")

import duckbill
from duckbill import Account, Subscription, Event
import duckbill.config

CLERK = duckbill.config.makeClerk()
SQL = CLERK.storage.dbc

