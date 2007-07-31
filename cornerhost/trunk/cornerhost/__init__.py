"""
object model for cornerhost automation
"""
# regexp used by domain and EmailRule
# @TODO: emailRE really ought to be pytypes.Email
# test is in EmailRule
emailRE = "^" \
          r"(%1|%2|%3|\w|-|\+)+(\.|%1|%2|%3|\w|-|\+)*@(\w|-)+(\.(\w|-)+)" \
          r'|pop_(\w|-)+' \
          r'|alias_(\w|-)+' \
          r'|error:nouser' \
          r'|~' \
          "$"

from schema import *
import config

#@TODO: just load these explicitly from python
from NewSiteGrunt import *
from BandwidthGrunt import *

from MailerApp import MailerApp
from UserApp import UserApp
from AdminApp import AdminApp
