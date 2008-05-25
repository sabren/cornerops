# site-related features
from cornerhost import Site
from strongbox import BoxView
from platonic import Intercept
from panel import ControlPanelFeature
from cornerhost import safety
import handy

#@abstract
class SiteFeature(ControlPanelFeature):
    pass

## commands ######################################

class DeleteSiteCommand(SiteFeature):
    def invoke(self, _clerk, _user, name):
        s = safety.safeSiteByName(_user, name)

        # force load of real domain object:
        assert s.domain.name == name

        # unhook domain:
        s.domain.site = None
        _clerk.store(s.domain)
        s.domain = None

        # unhook aliases:
        for a in s.aliases[:]:
            a.site = None
            s.aliases.remove(a)
            _clerk.store(a)
            
        _clerk.delete(Site, s.ID)
        _user.getBeaker().mqsend('genhttpconf')

class SaveSiteCommand(SiteFeature):
    def _assignExtra(self, site, extra):
        pass # only admin can do this

    def invoke(self, _clerk, _user, name, haserrs=0, suExec=0, docroot='', extra=None):
        
        s = safety.safeSiteByName(_user, name)
        try:
            s.docroot = docroot
            assert not hasattr(s.private, "isStub"), "set_docroot didn't clear .isStub"
            assert s.docroot == docroot
            s.haserrs = haserrs
            s.suExec = suExec
            self._assignExtra(s, extra)
        except (ValueError, TypeError), e:
            raise Intercept(e)
        
        _clerk.store(s)
        _user.getBeaker().mqsend('genhttpconf')
        

class AdminSaveSiteCommand(SaveSiteCommand):
    def _assignExtra(self, site, extra):
        site.extra = extra
