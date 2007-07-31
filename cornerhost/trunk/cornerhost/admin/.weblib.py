import sys, os
def carp():
    sys.stderr = sys.stdin
    print "content-type: text/plain"
    print 
#carp()

import sesspool
import cornerhost.config


## set up session
pool = sesspool.SessPool("sess/sessions.db")
SESS = sesspool.Sess(pool, REQ, RES)
SESS.start()
ENG.do_on_exit(SESS.stop)


CLERK = cornerhost.config.makeClerk()
