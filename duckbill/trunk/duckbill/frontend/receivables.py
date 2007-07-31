from shared import *
import zebra
from duckbill import Account, Receivables


if __name__=="__main__":

    only_overdue = REQ.get("overdue") is not None

    model = {"errors":[],
             "rows":[],
             "only_overdue": only_overdue}

    r = Receivables(SQL, CLERK)

    coltotals = [0,0,0,0]
    grandtotal = 0

    for acc in r.dueAccounts():
        aging = r.separate_ages(acc.aging())
        rowtotal = 0
        
        if ((aging[0]+aging[1]+aging[2])==0) and only_overdue:
            continue
        else:
            for i in range(len(aging)):
                coltotals[i] += aging[i]
                rowtotal += aging[i]
                grandtotal += aging[i]

        model["rows"].append({"aging": aging,
                              "account": acc,
                              "rowtotal": rowtotal})

    model["coltotals"] = coltotals
    model["grandtotal"] = grandtotal
    print >> RES, zebra.fetch("receivables", model)
