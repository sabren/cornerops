from cornerhost.features import dns
from cornerhost.schema import Domain, Site
import personas
import unittest

class DNSFeaturesTest(unittest.TestCase):

    def setUp(self):
        self.uc = personas.fredClerk()
        self.user = self.uc.user
        self.clerk = self.uc.clerk
        self.dom = self.user.domains[0]

    def test_DeleteDomainCommand(self):
        domName = 'del.com'
        dns.CreateDomainCommand().invoke(self.clerk, self.user, domName=domName)
        dns.DeleteDomainCommand().invoke(self.clerk, self.user, name=domName)
        assert not self.clerk.match(Domain, domain=domName)
        
    def test_DeleteDomainCommand_with_site(self):
        # prevent you from deleting a domain with a site
        cmd = dns.DeleteDomainCommand()
        self.dom.site = Site(domain = self.dom)
        self.assertRaises(AssertionError, cmd.invoke, self.clerk, self.user,
                          name='fred.com')

    def test_DeleteDomainCommand_with_subdomain(self):
        # prevent you from deleting a domain with subdomain        
        cmd = dns.DeleteDomainCommand()
        self.dom.subs << Domain(domain="sub.fred.com")
        self.assertRaises(AssertionError, cmd.invoke,
                          self.clerk, self.user, name='fred.com')

    def test_RepointDomainCommand(self):
        cmd = dns.RepointDomainCommand()
        req = {"name":"fred.com", "repoint_to":"new_site"}
        # adding new_site should fail: fred.com already has site:
        self.assertRaises(AssertionError, cmd.invoke,
                          self.clerk, self.user, **req)

        # @TODO: encapsulate this site deletion junk:
        del self.user.sites[0]
        self.dom.site = None

        # with the site gone, the Command should work:
        cmd.invoke(self.clerk, self.user, **req)
        assert self.dom.site.user is self.user
        assert self.dom.site.domain is self.dom

        #should fail on duplicate site:
        self.assertRaises(AssertionError, cmd.invoke,
                          self.clerk, self.user, **req)


    def test_save_domain(self):
        self.dom.processmail = True
        cmd = dns.SaveDomainCommand()
        cmd.invoke(self.clerk, self.user,
            name="fred.com",
            rule="point",
            rectype="cname",
            location="cname.com")
        assert not self.dom.processmail
        assert self.dom.rule == "point"
        assert self.dom.location == "cname.com"
        assert self.dom.rectype == "cname"

    def test_save_dnsrec_txt(self):        
        assert len(self.dom.dnsrecs)==0
        cmd = dns.SaveDNSRecCommand()
        cmd.invoke(self.clerk, self.user,
            ID=None,            
            domain='fred.com',
            rectype='TXT',
            priority=0,
            value='SPLORNK')
        assert len(self.dom.dnsrecs)==1
        
    def test_save_dnsrec_mx(self):        
        assert len(self.dom.dnsrecs)==0
        cmd = dns.SaveDNSRecCommand()
        cmd.invoke(self.clerk, self.user,
            ID=None,            
            domain='fred.com',
            rectype='MX',
            priority=2,
            value='splornk.net')
        assert len(self.dom.dnsrecs)==1
        
    def test_CreateDomainCommmand(self):
        cmd = dns.CreateDomainCommand()
        cmd.invoke(self.clerk, self.user, domName='xyz.com', create_site=False)
        assert self.uc.safeDomain('xyz.com').site is None
        cmd.invoke(self.clerk, self.user, domName='site.com', create_site=True)
        assert self.uc.safeDomain('site.com').site is not None

    def test_CreateSubdomainCommand(self):
        cmd = dns.CreateSubdomainCommand()
        cmd.invoke(self.clerk, self.user,
                   subName='sub',domName='fred.com', create_site=False)
        assert self.uc.safeDomain('sub.fred.com').site is None
        cmd.invoke(self.clerk, self.user,
                   subName='subsite',domName='fred.com', create_site=True)
        assert self.uc.safeDomain('subsite.fred.com').site is not None

    def test_repoint(self):
        alias = 'alias.com'
        dns.CreateDomainCommand().invoke(self.clerk, self.user,
            domName=alias, create_site=False)
        
        cmd = dns.RepointDomainCommand()
        cmd.invoke(self.clerk, self.user, name=alias, repoint_to='new_site')
        dom = self.uc.safeDomain(alias)
        assert dom.site.user is self.user
        assert dom.site.domain is dom
        # should fail on duplicate site:
        self.assertRaises(AssertionError, cmd.invoke, self.clerk, self.user,
                          name=alias, repoint_to="new site")
        

if __name__=="__main__":
    unittest.main()
