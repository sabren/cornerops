from cornerhost.schema import Site
from cornerhost.features import site
from platonic import Intercept
import unittest
import personas

class SiteFeaturesTest(unittest.TestCase):
    
    def test_DeleteSiteCommand(self):
        uclerk = personas.fredClerk()

        self.assertEquals(1, len(uclerk.clerk.match(Site)))

        cmd = site.DeleteSiteCommand()
        cmd.invoke(_clerk=uclerk.clerk, _user=uclerk.user, name='fred.com')

        sites = uclerk.clerk.match(Site)
        #import pdb; pdb.set_trace()
        self.assertEquals([], sites)
        self.assertEquals(0, len(uclerk.clerk.match(Site)))

    def test_SaveSiteCommand(self):
        uclerk = personas.fredClerk()
        oldSiteExtra = uclerk.clerk.fetch(Site).extra
        site.SaveSiteCommand().invoke(
            _clerk=uclerk.clerk,_user=uclerk.user,
            name='fred.com', haserrs=0, suExec=1, docroot='top',
            extra='this should be ignored')
        
        newSite = uclerk.clerk.fetch(Site)
        assert newSite.extra == oldSiteExtra
        assert newSite.suExec
        assert not newSite.haserrs
        self.assertEquals("top", newSite.docroot)

    def test_SaveSiteCommand_bad(self):
        uclerk = personas.fredClerk()
        self.assertRaises(Intercept,
            site.SaveSiteCommand().invoke,
                          _clerk=uclerk.clerk,_user=uclerk.user,
                          name='fred.com', haserrs=0, suExec=1, docroot='$@!?')

    def test_AdminSaveSiteCommand(self):
        uclerk = personas.fredClerk()
        site.AdminSaveSiteCommand().invoke(
            _clerk=uclerk.clerk,_user=uclerk.user,
            name='fred.com', haserrs=0, suExec=1, docroot='top',
            extra='valid admin extra')
        newSite = uclerk.clerk.fetch(Site)
        assert newSite.extra == 'valid admin extra'
        assert newSite.suExec
        assert not newSite.haserrs
        self.assertEquals("top", newSite.docroot)


if __name__=="__main__":
    unittest.main()
