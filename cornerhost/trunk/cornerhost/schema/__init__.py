from DNSRec import DNSRec
from EmailRule import EmailRule
from Mailbox import Mailbox
from Site import Site
from Domain import Domain
from Server import Server
from Trail import Trail
from Usage import Usage
from Plan import Plan
from Database import Database
from User import User
from Signup import Signup
Server.users.type = User
Site.user.type = User
Site.domain.type = Domain
Site.aliases.type = Domain
EmailRule.domain.type = Domain
DNSRec.domain.type = Domain
Domain.user.type = User
Domain.zone.type = Domain
Domain.subs.type = Domain
Usage.user.type = User
Mailbox.user.type = User
Database.user.type = User
