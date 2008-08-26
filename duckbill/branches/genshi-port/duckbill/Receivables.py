from pytypes import FixedPoint, Date
from duckbill import Account

class Receivables:
    """
    I report on receivables for the system.
    """
    def __init__(self, dbc, clerk):
        self.dbc = dbc
        self.clerk = clerk


    def dueAccounts(self):
        res = []
        for row in self.query_receivables():
            accID, account, balance = row
            if balance > 0:
                acc = self.clerk.fetch(Account, ID=accID)
                res.append( acc )
        return res


    def query_receivables(self):
        """
        returns a list of (accID, account, due) tuples
        """
        cur = self.dbc.cursor()
        cur.execute(
            """
            SELECT a.ID, a.account, sum(e.amount * re.spin) as due
            FROM bill_event e, bill_account a, ref_event re
            WHERE e.accountID = a.ID
              AND e.event = re.event
              AND a.status != 'closed'
            GROUP BY a.account
            HAVING due > 0 
            ORDER BY due DESC, a.account
            """)
        return cur.fetchall()


    def separate_ages(self, events, binsize=15, maxbins=4):
        """
        separates an account's aged receivables into bins
        """
        # generate maxbins bins, oldest first:
        bins = []
        for x in range(0, maxbins):
            bins.append(Date("today") - (binsize*x))        
        bins.reverse()

        # separate values according to dates
        # (note that this ignores anything posted in the future)
        # (but then there should never be anything in the future)
        vals = [0] * len(bins)   
        for evt in events:
            for i in range(len(bins)):
                islastbin = (i==len(bins)-1)
                if (evt.posted <= bins[i]) or (islastbin):
                    vals[i] += evt.value
                    break
        return vals

