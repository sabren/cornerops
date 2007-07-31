
assert REQ["username"] == USER.username, "not your chart"
from cornerhost.bandwidthchart import showchart
showchart(REQ, RES, CLERK)

