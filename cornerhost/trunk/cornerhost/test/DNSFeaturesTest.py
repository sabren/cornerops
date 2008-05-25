from cornerhost.features import dns
from cornerhost.schema import Domain, Site
import personas
import unittest

class DNSFeaturesTest(unittest.TestCase):

    def setUp(self):
        self.uc = personas.fredClerk()
        self.dom = self.uc.user.domains[0]

    def test_DeleteDomainCommand(self):
        domName = 'del.com'
        dns.CreateDomainCommand(self.uc).invoke(domName=domName)
        dns.DeleteDomainCommand(self.uc).invoke(name=domName)
        assert not self.uc.clerk.match(Domain, domain=domName)
        
    def test_DeleteDomainCommand_with_site(self):
        # prevent you from deleting a domain with a site
        cmd = dns.DeleteDomainCommand(self.uc)
        self.dom.site = Site(domain = self.dom)
        self.assertRaises(AssertionError, cmd.invoke, name='fred.com')

    def test_DeleteDomainCommand_with_subdomain(self):
        # prevent you from deleting a domain with subdomain        
        cmd = dns.DeleteDomainCommand(self.uc)
        self.dom.subs << Domain(domain="sub.fred.com")
        self.assertRaises(AssertionError, cmd.invoke, name='fred.com')

    def test_RepointDomainCommand(self):
        cmd = dns.RepointDomainCommand(self.uc)
        req = {"name":"fred.com", "repoint_to":"new_site"}
        # adding new_site should fail: fred.com already has site:
        self.assertRaises(AssertionError, cmd.invoke, **req)

        # @TODO: encapsulate this site deletion junk:
        del self.uc.user.sites[0]
        self.dom.site = None

        # with the site gone, the Command should work:
        cmd.invoke(**req)
        assert self.dom.site.user is self.uc.user
        assert self.dom.site.domain is self.dom

        #should fail on duplicate site:
        self.assertRaises(AssertionError, cmd.invoke, **req)


    def test_save_domain(self):
        self.dom.processmail = True
        cmd = dns.SaveDomainCommand(self.uc)
        cmd.invoke(
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
        cmd = dns.SaveDNSRecCommand(self.uc)
        cmd.invoke(
            ID=None,            
            domain='fred.com',
            rectype='TXT',
            priority=0,
            value='SPLORNK')
        assert len(self.dom.dnsrecs)==1
        
    def test_save_dnsrec_mx(self):        
        assert len(self.dom.dnsrecs)==0
        cmd = dns.SaveDNSRecCommand(self.uc)
        cmd.invoke(
            ID=None,            
            domain='fred.com',
            rectype='MX',
            priority=2,
            value='splornk.net')
        assert len(self.dom.dnsrecs)==1
        
    def test_CreateDomainCommmand(self):
        cmd = dns.CreateDomainCommand(self.uc)
        cmd.invoke(domName='xyz.com', create_site=False)
        assert self.uc.safeDomain('xyz.com').site is None
        cmd.invoke(domName='site.com', create_site=True)
        assert self.uc.safeDomain('site.com').site is not None

    def test_CreateSubdomainCommand(self):
        cmd = dns.CreateSubdomainCommand(self.uc)
        cmd.invoke(subName='sub',domName='fred.com', create_site=False)
        assert self.uc.safeDomain('sub.fred.com').site is None
        cmd.invoke(subName='subsite',domName='fred.com',
                   create_site=True)
        assert self.uc.safeDomain('subsite.fred.com').site is not None

    def test_repoint(self):
        alias = 'alias.com'
        dns.CreateDomainCommand(self.uc).invoke(
            domName=alias, create_site=False)
        
        cmd = dns.RepointDomainCommand(self.uc)
        cmd.invoke(name=alias, repoint_to='new_site')
        dom = self.uc.safeDomain(alias)
        assert dom.site.user is self.uc.user
        assert dom.site.domain is dom
        # should fail on duplicate site:
        self.assertRaises(AssertionError, cmd.invoke,
                          name=alias, repoint_to="new site")
        

if __name__=="__main__":
    unittest.main()
