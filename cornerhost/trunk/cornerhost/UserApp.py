from cornerhost.grunts import UserClerk
from cornerhost.features import panel, site, dns, email, remote, user
import logging
from platonic import AbstractApp
import tiles
import weblib

class DictWrap:
    """
    missing values default to '0'
    use case: checkbox values from a form going into
    the redirect expression. eg: ?bool=%(bool)s
    if bool is unchecked, then nothing gets passed in,
    so a normal dict would raise a keyerror. instead,
    this just returns a '0'...

    Ideally, the default would be '' or it would be
    parsed from the __expected__ parameter, but
    @TODO: the code that handles __expected__ is gone!

    However, since this is currently only used for
    checkboxes, it does the job...
    """
    def __init__(self, d):
        self.d = d
    def __getitem__(self, key):
        return self.d.get(key, '0')


class CornerApp(AbstractApp):

    def __init__(self, default=None):
        super(CornerApp, self).__init__()
        self.tiles = tiles.makeUserWebMap()
        self.defaultAction = default
        self.bounceTo = {} # where to go after intercept
        self.success = {} # or after success
        self.featureSet = {}


    def buildFeature(self, req):
        return self.featureFromAction(
            req.get("action", self.defaultAction).replace(" ","_"))


    def featureFromAction(self, action):
        assert action in self.featureSet, "unknown action: %s" % action
        feature = self.featureSet[action]
        feature.action = action
        return feature

        
    def invoke(self, req, res, feature, model=None):

        if model is None:
            model = self.prepareModel(req)
            
        result = feature(self.clerk).handle(req, res, self.sess)
        if result is None:
            raise weblib.Redirect(self.success[feature.action] % DictWrap(req))
        elif isinstance(result,dict) or isinstance(result, Model):
            model.update(result)
        else:
            raise TypeError(
                "result should be none or Model, not %s" % result)

        return model


    def prepareModel(self, req):
        return {'req':req}


    def render(self, req, res, feature, model):
        res.write(self.tiles[feature.action]().render(model))


    def whereToGoWhenIntercepted(self, action):
        return self.bounceTo.get(action)


    def onIntercept(self, req, res, feature, e):
        "e= intercept; feature=the feature we were trying"
        bounceTo = self.whereToGoWhenIntercepted(feature.action)
        model = self.prepareModel(req)
        model.update(e.data) # for {:error:}
        feature2 = self.featureFromAction(bounceTo)
        model.update(self.invoke(req, res, feature2, model))
        self.render(req, res, feature2, model)


class UserApp(CornerApp):

    def addScreen(self, action, model=None):
        self.featureSet[action] = model or panel.EmptyModel

    def addCommand(self, action, command, onIntercept=None, onSuccess=None):
        self.featureSet[action] = command
        self.bounceTo[action] = onIntercept
        self.success[action] = onSuccess

    def __init__(self, uobj, clerk, sess, isAdmin=False):
        super(UserApp, self).__init__(default="list_sites")
        
        # @TODO: need self.clerk because CornerApp uses it. ugh :(
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
        c('create_database', remote.CreateDatabaseCommand,
          "list_databases",
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
        model["jumpto"] = None
        logging.debug("username is %s" % self.uclerk.user.username)
        logging.debug("model has: %s" % model.keys())
        return model

