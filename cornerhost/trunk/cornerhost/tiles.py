
from genshi.template import TemplateLoader

class SimpleTile:
    def render(self, model):
        return model.out

class GenshiTile(SimpleTile):
    loader = TemplateLoader(['../skin'], variable_lookup='lenient')

    def __init__(self, filename):
        self.filename = filename

    def render(self, model):
        tpl = self.loader.load(self.filename)
        stream = tpl.generate(**model)
        return stream.render().encode("utf-8")

def makeUserWebMap():
    return {
        "list_boxes"   : lambda : GenshiTile("boxes.gen"),
        "list_databases":lambda : GenshiTile("databases.gen"),
        "list_sites"   : lambda : GenshiTile("sites.gen"),
        "add_domain"   : lambda : GenshiTile("add_domain.gen"),
        "add_subdomain": lambda : GenshiTile("add_subdomain.gen"),
        "added_domain" : lambda : GenshiTile("added_domain.gen"),
        "delete_box"   : lambda : GenshiTile("delete_box.gen"),
        "delete_db"    : lambda : GenshiTile("delete_db.gen"),
        "edit_dns_mx"  : lambda : GenshiTile("frm_dns_mx.gen"),
        "edit_dns_txt" : lambda : GenshiTile("frm_dns_txt.gen"),
        "edit_site"    : lambda : GenshiTile("frm_site.gen"),
        "list_domains" : lambda : GenshiTile("dns.gen"),
        "edit_domain"  : lambda : GenshiTile("frm_domain.gen"),
        "analog"       : lambda : SimpleTile(),
        "email"        : lambda : GenshiTile("email_rules.gen"),
        "add_rule"     : lambda : GenshiTile("frm_rule.gen"),
        "edit_rule"    : lambda : GenshiTile("frm_rule.gen"),
        "edit_catchall": lambda : GenshiTile("frm_catchall.gen"),
        "cron"         : lambda : GenshiTile("cron.gen"),
        "password"     : lambda : GenshiTile("password.gen"),
        "show_box"     : lambda : GenshiTile("mailbox.gen"),
        "show_database": lambda : GenshiTile("database.gen"),
    }
