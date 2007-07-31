
import os, re
import handy

class MySQL(object):
    """
    This class is here so users can set up and delete
    databases from the control panel. It talks directly
    to the MySQL server.
    """
    def __init__(self):
        self.dbc = None
    
    ## used by control panel #########################################

    def setPassword(self, username, password):
        self.execute(
            """
            UPDATE user
            SET password=password('%s')
            WHERE user = '%s'
            """ % (self.sanitize(password),
                   self.sanitize(username)))
        self.flushPrivileges()


    def createDatabase(self, username, dbname):
        # guards:
        if not re.match(r"%s_\w+" % username, dbname):
            raise ValueError("invalid database name")
        if self.has_db(dbname):
            raise ValueError("database '%s' exists" % dbname)
        
        # still here, so:
        self.execute("CREATE DATABASE %s" % self.sanitize(dbname))
        password = self.grantPermissions(dbname, username)
        self.flushPrivileges()
        return password


    def dropDatabase(self, username, dbname):
        # guards:
        if not re.match(r"%s_\w+" % username, dbname):
            raise ValueError("invalid database name")
        if not self.has_db(dbname):
            raise ValueError("database '%s' doesn't exist to begin with"
                             % dbname)
        self.execute("DROP DATABASE %s" % self.sanitize(dbname))
        self.execute("DELETE FROM db where db='%s'" % self.sanitize(dbname))
        self.flushPrivileges()

        
    ## internal ######################################################

    def flushPrivileges(self):
        self.execute("FLUSH PRIVILEGES")

    def has_db(self, dbname):
        cur = self.execute("show databases like '%s'" % self.sanitize(dbname))
        return bool(cur.fetchall())

    def grantPermissions(self, dbname, username):
        host = self.okHost(username) or "%.sabren.com"
        
        sql =\
            """
            GRANT SELECT, INSERT, UPDATE, DELETE,
                  CREATE, CREATE TEMPORARY TABLES,
                  DROP, INDEX, ALTER, LOCK TABLES
            ON %s.*
            TO %s@'%s'
            """ % (self.sanitize(dbname),
                   self.sanitize(username), self.sanitize(host))
        
        if host:
            password = '?'
        else:
            password = handy.randpass()
            sql += "IDENTIFIED BY '%s'" % password

        self.execute(sql)

        # and this is so the db table ONLY has '%' in it
        self.execute("update db set host='%'")
        return password
        

    def okHost(self, username):
        """
        returns the host that the user can log in from.
        """
        cur = self.execute("select user, host from user where user='%s'"
                           % self.sanitize(username))
        all = cur.fetchall()
        if len(all) == 0:
            return None
        elif len(all)==1:
            return all[0][1]
        else:
            raise Exception(
               "user should not have multiple user entries (%s)" % len(all))

    ## utility routines ##############################################

    def execute(self,sql):
        cur = self.cursor()
        cur.execute(sql)
        return cur

    def cursor(self):
        if not self.dbc:
            import sqlRoot
            self.dbc = sqlRoot.connect()
        return self.dbc.cursor()

    def sanitize(self, s):
        assert type(s) in (str, unicode), "%s is not a string" % repr(s)
        return s.replace("'","''")

