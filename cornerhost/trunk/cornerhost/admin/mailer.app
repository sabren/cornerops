from cornerhost import MailerApp
from cornerhost.tiles import CompositeTile, ZebraTile, SimpleTile
ZebraTile.path = "../skin"
model = {}
RES.write(ZebraTile("header.zb").render(model))
RES.write(ZebraTile("adminbar.zb").render(model))
print >> RES, MailerApp(REQ, CLERK).act()
RES.write(ZebraTile("footer.zb").render(model))
