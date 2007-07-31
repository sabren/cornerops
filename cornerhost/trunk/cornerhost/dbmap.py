
from cornerhost import *
import duckbill.config

DBMAP = {
    User: "sys_user",
    User.account: "accountID",
    User.server: "serverID",
    User.plan:"planID",

    Plan: "sys_plan",

    Usage: "sys_user_traffic",
    Usage.user: "userID",

    Site: "sys_site",
    Site.domain: "domainID",
    Site.user: "userID",

    Domain: "sys_domain",
    Domain.user: "userID",
    Domain.site: "siteID",
    Domain.zone: "zoneID",

    DNSRec: "sys_domain_mx",
    DNSRec.domain: "domainID",

    EmailRule: "sys_forward",
    EmailRule.domain: "domainID",   
    
    Mailbox: "sys_mailbox",
    Mailbox.user: "userID",

    Database: "sys_database",
    Database.user: "userID",
    
    Signup: "sale_prospect",
    Trail: "sys_trail",
    Server: "sys_server",
}

DBMAP.update(duckbill.config.schema.dbmap)
