# email related features
from cornerhost.schema import EmailRule, Mailbox, Plan
from cornerhost import safety
from panel import ControlPanelFeature, extractNewPass
from strongbox import BoxView
from xmlrpclib import Fault
from platonic import Model, Intercept

#@abstract
class EmailFeature(ControlPanelFeature):
    pass

class SessionFeature(EmailFeature):
    passVar = "box_password"

## commands ######################################

class DeleteRuleCommand(EmailFeature):
    def invoke(self, _user, _clerk, oldDom, ID):
        old = safety.safeDomain(_user, oldDom)
        rule = safety.safeEmailRuleByID(old,ID)
        _clerk.delete(EmailRule,rule.ID)
        _user.getBeaker().genmailconf()

#@abstract
class SaveRuleFeature(EmailFeature):

    def ruleMessage(self, e):
        field, value = e[0], e[1]
        if field=="virtuser":
            msg = "invalid mailbox name: %s" % value 
        elif field=="dupe":
            msg = "there is already a rule for %s" % value
        elif field=="catchall":
            msg = value
        else:
            msg = "invalid forwarding address"
        return msg


    def compileRule(self, rule, mailto):
        if rule =="bounce":
            return EmailRule.BOUNCE
        elif rule=="main":
            return "~"
        elif rule in ["mapto", "forward"]:
            if mailto=="someone@else.com":
                raise ValueError('forwarding address', 'enter a real address')
            else:
                return mailto
        elif rule.startswith("pop_"):
            return rule
        else:
            raise AssertionError, "unknown rule type"


class SaveRuleCommand(SaveRuleFeature):
    def checkDuplicate(self, rule, dom):
        #@TODO: move this to EmailRule itself on set_domain
        dupes = [dupe for dupe in dom.rules
                 if (rule.virtuser==dupe.virtuser) and (dupe is not rule)]
        if dupes:
            raise ValueError("dupe",
                "%s@%s" % (rule.virtuser, dom.domain))

    def do_save_rule(self,_clerk,_user, ID, virtuser, oldVirt, domName, mailto):
        #@TODO: there's a dependency here that I don't know how to expose.
        #If the rule attributes are changed before dom is loaded,
        #clerk won't save the rule. same thing with rule.dom=domain (vs <<)
        #however, I couldn't duplicate this in the test case

        dom = safety.safeDomain(_user, domName)
        if ID:
            rule = safety.safeEmailRuleByID(dom, ID)
        elif oldVirt:
            rule = safety.safeEmailRule(dom, oldVirt)
        else:
            rule = EmailRule()
        
        rule.virtuser=virtuser
        rule.mailto=mailto
        
        self.checkDuplicate(rule, dom)

        if rule not in dom.rules:
            dom.rules << rule
            
        _clerk.store(dom)
        _user.getBeaker().genmailconf()

    def invoke(self, _clerk, _user, domName, mailto,
               rule='~', ID=0, virtuser='', oldVirt=''):
        if not virtuser.strip():
            raise Intercept("no mailbox name given")
        try:
            self.do_save_rule(
                _clerk=_clerk,
                _user=_user,
                ID = ID,
                virtuser = virtuser,
                oldVirt = oldVirt,
                domName = domName,
                mailto = self.compileRule(rule, mailto))
        except ValueError, e:
            raise Intercept(self.ruleMessage(e))


class SaveCatchallCommand(SaveRuleFeature):
    
    def invoke(self, _user, _clerk, domName, rule, mailto):
        try:
            dom = safety.safeDomain(_user, domName)
            dom.mailto=self.compileRule(rule, mailto)
            _clerk.store(dom)
            _user.getBeaker().genmailconf()
        except ValueError, e:
            raise Intercept(self.ruleMessage(e))


class CreateBoxCommand(SessionFeature):
    def invoke(self, _clerk, _user, _sess, mailbox):
        if _user.plan.boxquota == Plan.UNLIMITED:
            pass
        else:
            assert _user.plan.boxquota != Plan.FORBIDDEN, \
                   "You don't have rights to add a new mailbox"
            assert len(_user.boxes) < _user.boxquota, \
                   "Adding a mailbox would exceed your quota."

        boxname = mailbox
        
        ## ensure we have a boxname:
        if not boxname:
            raise Intercept("a mailbox name is requried.")
            
        ## first check for duplicates (any user)
        if _clerk.match(Mailbox, mailbox=boxname):
            raise Intercept("box %s already exists" % boxname)
            
        ## string validation
        try:
            box = _user.boxes << Mailbox(mailbox=boxname)
        except ValueError:
            raise Intercept("invalid mailbox name.")

        ## now add it:
        try:
            passwd = _user.getBeaker().addpop(box.mailbox)
        except Exception, e:
            assert False, e # @TODO: real error message
        _clerk.store(_user)
        _sess[SessionFeature.passVar] = passwd


class DeleteBoxCommand(ControlPanelFeature):
    def invoke(self, _clerk, _user, mailbox):
        box = safety.safeMailbox(_user, mailbox)
        _user.getBeaker().delpop(box.mailbox)

        for rule in box.rules:
            if rule.virtuser=='(catchall)':
                rule.domain.mailto = EmailRule.BOUNCE
                _clerk.store(rule.domain)
            else:
                rule.mailto=EmailRule.BOUNCE
                _clerk.store(rule)

        _clerk.delete(Mailbox, box.ID)


class SetBoxPasswordCommand(ControlPanelFeature):
    # tests in test/SetBoxPasswordCommandTest


    def invoke(self, _user, mailbox, pass1, pass2):
        #@TODO: clean this mess up. this used to be do_invoke
        # it's here so we can test exceptions in invoke_x
        #also, this should probably be in remote.py
        try:           
            return self.invoke_x(_user, mailbox, pass1, pass2)
        except (TypeError, ValueError, LookupError, IOError), e:
            raise Intercept(error=self.buildErrorMessage(e))

    
    def invoke_x(self, _user, mailbox, pass1, pass2):
        try:
            box = safety.safeMailbox(_user, mailbox)
        except AssertionError, e:
            raise LookupError(e)
        try:
            password = extractNewPass(pass1,pass2)
            _user.getBeaker().setboxpasswd(box.mailbox, password)
        except Fault, f:
            msg = f.faultString
            # trim "NO:" errors from beaker
            #@TODO: trap other beaker errors
            if msg.count("NO:"):
                msg = msg[msg.find("NO:"):]
            raise IOError(msg) # so we can catch it
