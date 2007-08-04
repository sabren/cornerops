-- MySQL dump 10.9
--
-- Host: db.sabren.com    Database: sei_cornerhost
-- ------------------------------------------------------
-- Server version	4.1.22-standard

--
-- Table structure for table bill_account
--

CREATE TABLE bill_account (
  ID int(11) NOT NULL auto_increment,
  brand enum('versionhost','cornerhost','dcd hosting') default 'cornerhost',
  old_is_active int(11) default NULL,
  fname varchar(50) default NULL,
  lname varchar(50) default NULL,
  email varchar(50) default NULL,
  email2 varchar(50) default NULL,
  phone varchar(50) default NULL,
  company varchar(50) default NULL,
  address1 varbinary(100) default NULL,
  address2 varchar(100) default NULL,
  city varchar(50) default NULL,
  state varchar(20) default NULL,
  postal varchar(10) default NULL,
  countryCD varchar(30) default NULL,
  customerID int(11) NOT NULL default '0',
  account varchar(32) NOT NULL default '',
  opened datetime default NULL,
  closed datetime default NULL,
  cycLen enum('month','year') default NULL,
  nextDue date default NULL,
  cardinfo text NOT NULL,
  autobill tinyint(1) NOT NULL default '0',
  lastfour varchar(4) default NULL,
  referredby varchar(32) default NULL,
  status varchar(32) default NULL,
  warned date default NULL,
  statementStrategy varchar(30) NOT NULL default 'always',
  PRIMARY KEY  (ID),
  UNIQUE KEY account (account),
  KEY email (email)
);

--
-- Table structure for table bill_event
--


CREATE TABLE bill_event (
  ID int(11) NOT NULL auto_increment,
  accountID int(11) NOT NULL default '0',
  subscriptionID int(11) default NULL,
  event varchar(16) default NULL,
  posted datetime default NULL,
  maturity date default NULL,
  amount decimal(8,2) default NULL,
  note varchar(255) default NULL,
  adminnote varchar(255) default NULL,
  source enum('bofa','paypal','check','other','n/a') default 'n/a',
  refnum varchar(32) default NULL,
  PRIMARY KEY  (ID)
);

--
-- Table structure for table bill_subscription
--


CREATE TABLE bill_subscription (
  ID int(11) NOT NULL auto_increment,
  accountID int(11) NOT NULL default '0',
  service varchar(30) default NULL,
  username varchar(30) default NULL,
  note varchar(255) default NULL,
  rate decimal(8,2) default NULL,
  opened date default NULL,
  closed date default NULL,
  cycLen enum('month','year') default NULL,
  nextDue date default NULL,
  status enum('active','closed') default 'active',
  PRIMARY KEY  (ID)
);
