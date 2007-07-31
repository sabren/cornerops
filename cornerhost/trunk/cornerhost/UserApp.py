
from cornerhost.grunts import UserClerk
from cornerhost.features import panel, site, dns, email, remote, user
import logging
import platonic

_ = panel.EmptyModel

class CornerApp(platonic.App):
    # overrides to add uclerk
    def initFeature(self, f, action):
        return f(self.clerk) #, self.sess)

    def invokeFeature(self, f, req, res):
        return f.handle(req, res, self.sess)

    def render(self, model, res, action):
        res.write(self.tiles[action]().render(model))

    def addScreen(self, action, model=_):
        self.featureSet[action] = model

    def addCommand(self, action, command, onIntercept, onSuccess=None):
        self.featureSet[action] = command
        if onIntercept:
            self.onIntercept(action, onIntercept)
        self.onSuccess(action, onSuccess)

class UserApp(CornerApp):

    def __init__(self, uobj, clerk, sess, isAdmin=False):
        super(UserApp, self).__init__(default="list_sites")
        
        # @TODO: need self.clerk because CornerApp usese it. ugh :(
        self.clerk = self.uclerk = UserClerk(uobj, clerk)
        self.sess = sess
        self.isAdmin=isAdmin

        s = self.addScreen
        c = self.addCommand
        ni = None # no intercept
        
        ### screens ####################
        
        s('add_domain')
        s('add_rule')
        s('add_subdomain')
        s('added_domain')
        s('admin')
        s('cron')
        s('delete_box')
        s('delete_db')
        s('edit_catchall')
        s('edit_dns_mx')
        s('edit_dns_txt')
        s('edit_domain') 
        s('edit_rule')
        s('edit_site')            
        s('email')
        s('list_boxes')
        s('list_databases')
        s('list_domains')
        s('list_sites')
        s('password')
        s('show_box')
        s('show_database')

        # special case for analog:
        s('analog', remote.AnalogFeature)

        ### commands ###################

        # remote, 5 commands
        c('create_database', remote.CreateDatabaseCommand, ni,
          "?action=list_databases&changed=1")
        c('set_password', remote.SetPasswordCommand, "password",
          "?action=password&changed=1")
        c('set_mysql_password', remote.SetMySQLPasswordCommand,
          'list_databases', "?action=list_databases&changed=1")
        c("really_delete_db", remote.DropDatabaseCommand, ni,
          "?action=list_databases&deleted=1")
        c('setcron', remote.SetCronCommand, "cron",
          "?action=cron&changed=1")

        # this should probably be in remote:
        c('set_box_password', email.SetBoxPasswordCommand, "show_box",
            "?action=list_boxes&changed=True")
        
        # email, 4 (+1) commands
        c('create_box', email.CreateBoxCommand, "list_boxes",
          "?action=show_box&mailbox=%(mailbox)s")
        c("really_delete_box", email.DeleteBoxCommand, ni,
          "?action=list_boxes&deleted=1")
        c('delete_rule', email.DeleteRuleCommand, ni,
          "?action=email&changed=1")
        c('save_new_rule', email.SaveRuleCommand, "add_rule",
          "?action=email&changed=1")
        c('save_rule', email.SaveRuleCommand, "edit_rule",
          "?action=email&changed=1")
        c('save_catchall', email.SaveCatchallCommand, "edit_catchall",
          "?action=email&changed=1")

        # dns, 8 commands
        c('create_domain', dns.CreateDomainCommand, "add_domain",
          "?action=added_domain&name=%(domName)s&hadSite=%(create_site)s")
        c('create_subdomain', dns.CreateSubdomainCommand, 'add_subdomain',
          "?action=added_domain&name=%(subName)s.%(domName)s&hadSite=%(create_site)s")
        c('delete_domain', dns.DeleteDomainCommand, ni,
          "?action=list_domains&changed=1")
        c('delete_record', dns.DeleteDNSRecCommand, ni,
          "?action=list_domains&changed=1")
        c('save_dns_mx', dns.SaveDNSRecCommand, "edit_dns_mx",
          "?action=list_domains")
        c('save_dns_txt', dns.SaveDNSRecCommand, "edit_dns_txt",
          "?action=list_domains")
        c('save_domain', dns.SaveDomainCommand, "edit_domain",
          "?action=edit_domain&name=%(name)s&changed=1")
        c('repoint', dns.RepointDomainCommand, ni,
          "?action=edit_domain&name=%(name)s&changed=1")
        
        # site, 2 commands
        c('delete_site', site.DeleteSiteCommand, ni,
          "?action=edit_domain&name=%(name)s")
        
        c('save_site', site.SaveSiteCommand, "edit_site",
          "?action=edit_site&name=%(name)s&changed=1")



    # overrides for other junk...
    def prepareModel(self, req):
        logging.debug("preparing model")
        model = {}
        model["req"] = req
        model["error"] = None
        model["admin"] = self.isAdmin
        model["user"] = self.uclerk.user
        model["changed"] = req.get("changed", None)
        model["sess"] = self.sess
        logging.debug("username is %s" % self.uclerk.user.username)
        logging.debug("model has: %s" % model.keys())
        return model

