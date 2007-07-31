
from reptile import Tile, SimpleTile, CompositeTile, ZebraTile

class UserPage(CompositeTile):
    def __init__(self, bodyTile):
        self.b = [bodyTile]
        
    def head(self):
        return [ZebraTile("header.zb"),
                ZebraTile("userbar.zb"),                
                ZebraTile("errors.zb")]
    
    def foot(self):
        return [ZebraTile("footer.zb")]
   
class AdminUserPage(UserPage):
    def head(self):
        return [ZebraTile("header.zb"),
                ZebraTile("adminbar.zb"),
                ZebraTile("userbar.zb"),
                ZebraTile("errors.zb")]

def makeUserWebMap(tileClass):
    return {
        "add_mailbox"  : lambda : tileClass(ZebraTile("frm_box.zb")),
        "list_boxes"   : lambda : tileClass(ZebraTile("boxes.zb")),
        "list_databases":lambda : tileClass(ZebraTile("databases.zb")),
        "list_sites"   : lambda : tileClass(ZebraTile("sites.zb")),
        "add_domain"   : lambda : tileClass(ZebraTile("add_domain.zb")),
        "add_subdomain": lambda : tileClass(ZebraTile("add_subdomain.zb")),
        "added_domain" : lambda : tileClass(ZebraTile("added_domain.zb")),
        "delete_box"   : lambda : tileClass(ZebraTile("delete_box.zb")),
        "delete_db"    : lambda : tileClass(ZebraTile("delete_db.zb")),
        "edit_dns_mx"  : lambda : tileClass(ZebraTile("frm_dns_mx.zb")),
        "edit_dns_txt" : lambda : tileClass(ZebraTile("frm_dns_txt.zb")),
        "newsite"      : lambda : tileClass(ZebraTile("newsite.zb")),
        "edit_site"    : lambda : tileClass(ZebraTile("frm_site.zb")),
        "list_domains" : lambda : tileClass(ZebraTile("dns.zb")),
        "edit_domain"  : lambda : tileClass(ZebraTile("frm_domain.zb")),
        "analog"       : lambda : SimpleTile(),
        "email"        : lambda : tileClass(ZebraTile("email.zb")),
        "add_rule"     : lambda : tileClass(ZebraTile("frm_rule.zb")),
        "edit_rule"    : lambda : tileClass(ZebraTile("frm_rule.zb")),
        "edit_catchall": lambda : tileClass(ZebraTile("frm_rule.zb")),
        "cron"         : lambda : tileClass(ZebraTile("cron.zb")),
        "password"     : lambda : tileClass(ZebraTile("password.zb")),
        "settings"     : lambda : tileClass(ZebraTile("settings.zb")),
        "show_box"     : lambda : tileClass(ZebraTile("mailbox.zb")),
        "show_database": lambda : tileClass(ZebraTile("database.zb")),
    }
