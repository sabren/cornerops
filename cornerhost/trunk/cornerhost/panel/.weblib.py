## import sys
## sys.stderr = sys.stdin
## print "content-type: text/plain"
## print 
VERBOSE_LOGS=False


## make sure we can load our modules:

## toggles whether we show error messages or not:
## also lets us fire off any special test mode stuff:
import os, logging
if os.path.exists("TEST_MODE.py"):
    import TEST_MODE
else:
    TEST_MODE = False


## error logging:
if VERBOSE_LOGS:
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log/%s.log' % os.getpid(),
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a')
else:
    #@TODO: this doesn't actually do anything yet... :)
    logging.basicConfig(
        level=logging.CRITICAL,
        filename="log/error.log",
        format='%(asctime)s %(levelname)s %(message)s',
        filemode='a')

##
import sys
#sys.path = ["/home/secure/lib", "/web/lib"] + sys.path

## just in CASE an uncaught error happens:
SITE_NAME="cornerhost controls"
SITE_MAIL="michal@sabren.com"

## use mysql? or plain old db file?
MYSQL_SESS = not TEST_MODE


## required modules:
import shelve
import weblib
import handy
import traceback
import cornerhost.schema
import cornerhost.config
import socket
import sesspool
from BeakerAuth import BeakerAuth
from weblib import Finished
import sesspool

def servername():
    """
    Return the short name of the server
    (eg, for scandium.sabren.com, returns scandium)
    """
    return socket.gethostname().split(".")[0]


def handleError(msg, user=None):
    RES.write(handy.trim(
        '''
        <html>
        <title>error</title>
        <style type="text/css">
        body, p, table {
            font-family: verdana, arial, helvetica;
            font-size: 10pt;
        }
        body {
            background: #eeeeee;
        }
        h1 {
           font-size: 10pt;
           background: gold;
           padding-left: 10px;
        }
        p { padding-bottom: 10px;
            padding-left: 10px;
            margin: 0px; }
        </style>
        </head>
        <div style="background: white">
          <h1>error</h1>
          <p>%s</p>
          <p style="color: gray">
           An email has been sent to the administrator.<br/>
           Please try back in a little while.
          </p>
        </div>
        ''') % msg)
    trace = "".join(traceback.format_exception(
        sys.exc_type, sys.exc_value, sys.exc_traceback))
    trace += "\n"
    trace += "query: %s\n" % str(REQ.query)
    trace += "form: %s\n" % str(REQ.form)
    trace += "session: %s\n" % str(SESS)
    if TEST_MODE:        
        RES.write("<pre>")
        RES.write(trace)
        RES.write("</pre>")
    RES.write("</html>")
    try:
        uname = getattr(user, "username", "(unknown)")
        handy.sendmail((handy.trim(
            """
            To: michal@sabren.com
            From: panel@sabren.com
            Subject: error in control panel

            user: %s
            this error was trapped with message:
            %s
            ------------------------------------
            """) % (msg, uname)) + trace)
    except:
        raise
        pass # oh well. 
    raise Finished


## SESS ########################################################
try:
    # define the sess pool:
    if MYSQL_SESS:
        import sqlWebSess
        pool = sesspool.SqlSessPool(
            sqlWebSess.connect())
    else:
        pool = sesspool.SessPool("sess/sessions.db")

    # now start the session:
    SESS = sesspool.Sess(pool, REQ, RES)
    SESS.start()
    ENG.do_on_exit(SESS.stop)
except:
    SESS=None
    handleError("There was an error creating your user session.")


## CLERK ######################################################
try:
    CLERK = cornerhost.config.makeClerk()
except:
    handleError("There was a problem connecting to the database.")

## USER #######################################################
try:
    auth = BeakerAuth(RES, SESS, CLERK)
    auth.check()
    USER = CLERK.fetch(cornerhost.schema.User, username=auth.key)
except Finished:
    raise 
except:
    handleError("There was a problem validating your login.")

