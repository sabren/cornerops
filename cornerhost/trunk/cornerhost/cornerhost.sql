-- MySQL dump 9.10
--
-- Host: db.sabren.com    Database: sei_cornerhost
-- ------------------------------------------------------
-- Server version	4.1.22-standard


--
-- Table structure for table `redirect`
--

CREATE TABLE redirect (
  username varchar(32) default NULL,
  oldserver varchar(32) default NULL,
  newserver varchar(32) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Table structure for table `ref_event`
--

CREATE TABLE ref_event (
  event varchar(30) default NULL,
  spin int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


--
-- Table structure for table `sale_prospect`
--

CREATE TABLE sale_prospect (
  ID int(11) NOT NULL auto_increment,
  TS datetime default NULL,
  fname varchar(32) default NULL,
  lname varchar(32) default NULL,
  email varchar(50) default NULL,
  company varchar(50) default NULL,
  phone varchar(32) default NULL,
  addr1 varchar(50) default NULL,
  addr2 varchar(50) default NULL,
  city varchar(20) default NULL,
  state varchar(20) default NULL,
  postal varchar(20) default NULL,
  country varchar(20) default NULL,
  username varchar(32) default NULL,
  domains text,
  plan varchar(20) default NULL,
  cycLen varchar(20) default NULL,
  spacex50 int(11) default NULL,
  ipaddress varchar(32) default NULL,
  service enum('web','cvs') default 'web',
  comments text,
  description text,
  payment enum('credit','paypal','check') default NULL,
  `status` enum('new','rejected','filled','cancelled') default NULL,
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=3143 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_database`
--

CREATE TABLE sys_database (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  dbname varchar(32) NOT NULL default '',
  PRIMARY KEY  (ID),
  UNIQUE KEY dbname (dbname)
) ENGINE=MyISAM AUTO_INCREMENT=715 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_domain`
--

CREATE TABLE sys_domain (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  zoneID int(11) NOT NULL default '0',
  siteID int(11) NOT NULL default '0',
  rule enum('host','point','friend') NOT NULL default 'host',
  domain varchar(128) character set utf8 default NULL,
  rectype enum('a','cname','friend') NOT NULL default 'a',
  location varchar(64) default NULL,
  mailto varchar(64) NOT NULL default '~',
  processmail tinyint(1) NOT NULL default '1',
  PRIMARY KEY  (ID),
  UNIQUE KEY domain_2 (domain),
  UNIQUE KEY domain (domain),
  UNIQUE KEY domain_3 (domain),
  UNIQUE KEY domain_4 (domain),
  UNIQUE KEY domain_5 (domain)
) ENGINE=MyISAM AUTO_INCREMENT=6185 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_domain_mx`
--

CREATE TABLE sys_domain_mx (
  ID int(11) NOT NULL auto_increment,
  domainID int(11) NOT NULL default '0',
  rectype enum('MX','TXT') default 'MX',
  priority int(11) NOT NULL default '0',
  `value` varchar(255) default NULL,
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=323 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_forward`
--

CREATE TABLE sys_forward (
  ID int(11) NOT NULL auto_increment,
  domainID int(11) NOT NULL default '0',
  virtuser varchar(32) NOT NULL default '',
  mailto varchar(64) default NULL,
  PRIMARY KEY  (ID),
  UNIQUE KEY domainID (domainID,virtuser)
) ENGINE=MyISAM AUTO_INCREMENT=8556 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_mailbox`
--

CREATE TABLE sys_mailbox (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  mailbox varchar(32) default NULL,
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=997 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_plan`
--

CREATE TABLE sys_plan (
  ID int(11) NOT NULL auto_increment,
  name varchar(30) default NULL,
  bandquota bigint(20) default NULL,
  diskquota bigint(20) default NULL,
  boxquota int(11) default '0',
  dbquota int(11) default '0',
  monthlyCost int(11) default NULL,
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_server`
--

CREATE TABLE sys_server (
  ID int(11) NOT NULL auto_increment,
  name varchar(32) default NULL,
  shortname char(2) default NULL,
  ipaddress varchar(15) default NULL,
  uptime varchar(50) default NULL,
  load1 decimal(5,2) default NULL,
  load5 decimal(5,2) default NULL,
  load15 decimal(5,2) default NULL,
  stamp timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  space varchar(5) default NULL,
  memory varchar(5) default NULL,
  `status` enum('active','inactive') default 'active',
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_site`
--

CREATE TABLE sys_site (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  domainID int(11) NOT NULL default '0',
  docroot varchar(255) default NULL,
  logdir varchar(255) default NULL,
  extra text,
  haslogs tinyint(1) NOT NULL default '1',
  haserrs tinyint(1) NOT NULL default '0',
  usealias tinyint(1) NOT NULL default '1',
  suExec tinyint(1) NOT NULL default '0',
  PRIMARY KEY  (ID),
  UNIQUE KEY domainID (domainID)
) ENGINE=MyISAM AUTO_INCREMENT=5630 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_trail`
--

CREATE TABLE sys_trail (
  ID int(11) NOT NULL auto_increment,
  `user` varchar(30) default NULL,
  what varchar(255) default NULL,
  tstamp datetime default NULL,
  server varchar(30) default NULL,
  note varchar(255) default NULL,
  PRIMARY KEY  (ID)
) ENGINE=MyISAM AUTO_INCREMENT=2177 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_user`
--

CREATE TABLE sys_user (
  ID int(11) NOT NULL auto_increment,
  serverID int(11) NOT NULL default '0',
  server_old varchar(50) default NULL,
  username varchar(32) NOT NULL default '',
  old_plan varchar(32) default NULL,
  planID int(11) NOT NULL default '0',
  diskquota int(11) default NULL,
  diskextra int(11) NOT NULL default '0',
  diskusing bigint(20) NOT NULL default '0',
  `status` enum('active','locked','closed') default 'active',
  is_active tinyint(1) NOT NULL default '1',
  bandquota bigint(20) default NULL,
  bandextra bigint(20) default '0',
  accountID int(11) NOT NULL default '0',
  bandrule enum('charge','disable') default 'charge',
  boxextra int(11) NOT NULL default '0',
  dbextra int(11) NOT NULL default '0',
  PRIMARY KEY  (ID),
  UNIQUE KEY username (username)
) ENGINE=MyISAM AUTO_INCREMENT=1398 DEFAULT CHARSET=latin1;

--
-- Table structure for table `sys_user_traffic`
--

CREATE TABLE sys_user_traffic (
  ID int(11) NOT NULL auto_increment,
  userID int(11) NOT NULL default '0',
  whichday date NOT NULL default '0000-00-00',
  traffic bigint(20) default NULL,
  PRIMARY KEY  (ID),
  UNIQUE KEY userID (userID,whichday)
) ENGINE=MyISAM AUTO_INCREMENT=651474 DEFAULT CHARSET=latin1;

