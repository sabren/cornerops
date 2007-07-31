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
        domName = s.domain.name

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

        # @TODO: this is how this SHOULD work:
        # 
        # # set all the slots, and then...
        # _clerk.store(s)
        #
        # ... Only that line doesn't save any Site records.
        # Instead, it saves ALL the domain records. There
        # seems to be something SERIOUSLY wrong with the
        # clerk object traversal logic. It works great for
        # simple cases, but it can't cope with an object
        # fetched from a chain of other objects (safety.safeSiteByName)
        #
        # This same problem is evident in the bizarre workarounds
        # for saving email rules (see comments in email.py)

        # so..
        # -----------------------------------------------

        # still use safety so we can trust the object
        s = safety.safeSiteByName(_user, name)

        # but then ignore that object graph and fetch
        # a new copy that clerk can actually handle.
        assert (Site, s.ID) in _clerk.cache, "not in cache"
        _clerk.cache.clear()
        # Note that simply deleting (Site, s.ID) is not sufficient!
        # Clerk still checks the cache for linked objects,
        # so it still winds up traversing all the old objects
        #
        # This indicates that the problem is with the other
        # objects in the graph, not the Site. My guess is
        # the problem is in user.Domain since ALL the domains
        # tend to get re-saved. 
        #
        # Somehow that triggers the overwrite of the Site object,
        # which indicates that perhaps the data from the Site
        # record is reloaded into memory, overwriting our object
        # before the new data can be saved...
        s = _clerk.fetch(Site, ID=s.ID)
        
        try:
            s.docroot = docroot
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
