-- MySQL dump 10.9
--
-- Host: db.sabren.com    Database: sei_cornerhost
-- ------------------------------------------------------
-- Server version	4.1.22-standard

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


--
-- Table structure for table `bill_account`
--

DROP TABLE IF EXISTS `bill_account`;
CREATE TABLE `bill_account` (
  `ID` int(11) NOT NULL auto_increment,
  `brand` enum('versionhost','cornerhost','dcd hosting') default 'cornerhost',
  `old_is_active` int(11) default NULL,
  `fname` varchar(50) default NULL,
  `lname` varchar(50) default NULL,
  `email` varchar(50) default NULL,
  `email2` varchar(50) default NULL,
  `phone` varchar(50) default NULL,
  `company` varchar(50) default NULL,
  `address1` varbinary(100) default NULL,
  `address2` varchar(100) default NULL,
  `city` varchar(50) default NULL,
  `state` varchar(20) default NULL,
  `postal` varchar(10) default NULL,
  `countryCD` varchar(30) default NULL,
  `customerID` int(11) NOT NULL default '0',
  `account` varchar(32) NOT NULL default '',
  `opened` datetime default NULL,
  `closed` datetime default NULL,
  `cycLen` enum('month','year') default NULL,
  `nextDue` date default NULL,
  `cardinfo` text NOT NULL,
  `autobill` tinyint(1) NOT NULL default '0',
  `lastfour` varchar(4) default NULL,
  `referredby` varchar(32) default NULL,
  `status` varchar(32) default NULL,
  `warned` date default NULL,
  `statementStrategy` varchar(30) NOT NULL default 'always',
  PRIMARY KEY  (`ID`),
  UNIQUE KEY `account` (`account`),
  KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=1451 DEFAULT CHARSET=latin1;

--
-- Table structure for table `bill_event`
--

DROP TABLE IF EXISTS `bill_event`;
CREATE TABLE `bill_event` (
  `ID` int(11) NOT NULL auto_increment,
  `accountID` int(11) NOT NULL default '0',
  `subscriptionID` int(11) default NULL,
  `event` varchar(16) default NULL,
  `posted` datetime default NULL,
  `maturity` date default NULL,
  `amount` decimal(8,2) default NULL,
  `note` varchar(255) default NULL,
  `adminnote` varchar(255) default NULL,
  `source` enum('bofa','paypal','check','other','n/a') default 'n/a',
  `refnum` varchar(32) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=31621 DEFAULT CHARSET=latin1;

--
-- Table structure for table `bill_subscription`
--

DROP TABLE IF EXISTS `bill_subscription`;
CREATE TABLE `bill_subscription` (
  `ID` int(11) NOT NULL auto_increment,
  `accountID` int(11) NOT NULL default '0',
  `service` varchar(30) default NULL,
  `username` varchar(30) default NULL,
  `password` varchar(30) default NULL,
  `note` varchar(255) default NULL,
  `rate` decimal(8,2) default NULL,
  `opened` date default NULL,
  `closed` date default NULL,
  `cycLen` enum('month','year') default NULL,
  `nextDue` date default NULL,
  `status` enum('active','closed') default 'active',
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=1743 DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

