import duckbill
import zebra
from strongbox import BoxView

clerk = duckbill.config.makeClerk()

data = {"errors":""}

data["locked"] = [{
    "account": a.account,
    "brand": a.brand,
    "balance": a.balance(),
    } for a in clerk.match(duckbill.Account, status="locked")]
data["locked"].sort(lambda a, b: -cmp(a["balance"], b["balance"]))

RES.write(zebra.fetch("locked.zb", data))
