# remote services (beaker)
import xmlrpclib

MOCKSERVER = "mockium"
MOCKPASSWD = "p455w0rd"

from MockBeaker import MockBeaker
from MockMySQL import MockMySQL

from MySQL import MySQL

def getBeaker(serverName):
    if serverName==MOCKSERVER:
        return MockBeaker()
    return xmlrpclib.ServerProxy("https://%s:45678" % serverName)


def getMySQL(serverName):
    if serverName==MOCKSERVER:
        return MockMySQL()
    else:
        return MySQL()
