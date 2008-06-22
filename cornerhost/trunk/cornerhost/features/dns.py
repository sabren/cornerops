# dns related features
from cornerhost import Domain, NewSiteGrunt, DNSRec
from strongbox import BoxView
from platonic import Intercept
from panel import ControlPanelFeature
from cornerhost import safety

#@abstract
class DNSFeature(ControlPanelFeature):
    pass

## commands ######################################

class SaveDNSRecCommand(DNSFeature):

    def invoke(self, domain, rectype, value, priority=0, ID=None):
        try:
            dom = safety.safeDomain(self.user, domain)
            if ID:
                rec = safety.safeDNSRec(dom, ID)
            else:
                rec = DNSRec()
            
            if rec.domain is not dom:
                dom.dnsrecs << rec
            rec.rectype = rectype
            rec.priority = priority # field might be disabled
            rec.value = value
            
            #@TODO: this is kludgy, but i can't put this in set_value
            # ...unless I split DNSRec into two classes...
            # ALSO, these should generally have a "." at the end!!
            from cornerhost.schema.Domain import reDomain
            if rectype=="MX" and not reDomain.match(rec.value):
                raise ValueError('value',rec.value)
            self.clerk.store(rec)
            
        except (ValueError, TypeError), e:
            raise Intercept(e)
        

class DeleteDomainCommand(DNSFeature):
    def invoke(self, name):
        dom = safety.safeDomain(self.user, name)
        #@TODO: cascading delete?
        #@TODO: real error handling, not assertions
        #(assertions should only check for things that can't happen)
        assert not dom.is_site, "delete the site first"
        assert not dom.subs, "delete the subdomains first"
        self.clerk.delete(Domain, dom.ID)        


class DeleteDNSRecCommand(DNSFeature):
    def invoke(self, domain_in, ID):
        rec = safety.safeDNSRec(safety.safeDomain(self.user, domain_in), ID)
        self.clerk.delete(DNSRec, rec.ID)


class CreateDomainCommand(DNSFeature):
    def makeDomainObject(self, domName, subName=None):
        return self.grunt.addDomain(domName)
    
    def invoke(self, domName, create_site=0, subName=''):
        try:
            #@TODO: NewSiteGrunt: ugh... :/
            self.grunt = NewSiteGrunt(self.clerk, self.user)
            dom = self.makeDomainObject(domName, subName)
        except (ValueError, TypeError), e:
            raise Intercept(e)
            
        if bool(int(create_site)):
            self.grunt.buildSite(dom.name)
            self.user.getBeaker().mqsend('genhttpconf')


class CreateSubdomainCommand(CreateDomainCommand):
    def makeDomainObject(self, domName, subName):
        return self.grunt.addSub(subName, domName)


class RepointDomainCommand(DNSFeature):
    def invoke(self, name, repoint_to):
        dom = safety.safeDomain(self.user, name)
        assert not dom.is_site, "%s already has its own site" % dom.name
        # merge the form logic with create_site in on_post_add_domain (above)
        if repoint_to=="new_site":
            NewSiteGrunt(self.clerk,
                         self.user).buildSite(name)
        else:
            dom.site = safety.safeSiteByName(self.user, repoint_to)
        self.clerk.store(dom)
        self.user.getBeaker().mqsend('genhttpconf')


class SaveDomainCommand(DNSFeature):
    def invoke(self, name, rule, rectype, location, processmail=0):
        try:
            dom = safety.safeDomain(self.user, name)
            dom.update(
                processmail = int(processmail),
                rule = rule,
                rectype = rectype,
                location = location)
            self.clerk.store(dom)
        except (TypeError, ValueError), e:
            raise Intercept(e)
