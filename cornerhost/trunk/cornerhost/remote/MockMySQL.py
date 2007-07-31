
class MockMySQL(object):
    # class var:
    dbs = {}
    pwd = {}

    def createDatabase(self, username, dbname):
        if dbname=='bad_name':
            raise ValueError, 'invalid name: %s' % dbname
        else:
            self.dbs.setdefault(username, [])
            self.dbs[username].append(dbname)


    def setPassword(self, username, password):
        self.pwd[username] = password
