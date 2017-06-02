-- phddb project
--
-- Michael Jeltsch, Khushbu Rauniyar
--
-- https://github.com/mjeltsch/phddb
--
-- MySQL database: phddb
--
-- Execute with mysql root privilieges:
-- mysql -u root -p < phddb.sql
--
CREATE DATABASE phddb;

GRANT ALL ON phddb.* TO phddb_user IDENTIFIED BY 'zdshDc6UZXnjUap6';

FLUSH PRIVILEGES;

USE phddb;

-- MySQL dump 10.13  Distrib 5.7.18, for Linux (x86_64)
--
-- Host: localhost    Database: phddb
-- ------------------------------------------------------
-- Server version	5.7.18-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `citations`
--

DROP TABLE IF EXISTS `citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citations` (
  `paper_id` mediumint(9) NOT NULL,
  `1980` int(5) DEFAULT NULL,
  `1981` int(5) DEFAULT NULL,
  `1982` int(5) DEFAULT NULL,
  `1983` int(5) DEFAULT NULL,
  `1984` int(5) DEFAULT NULL,
  `1985` int(5) DEFAULT NULL,
  `1986` int(5) DEFAULT NULL,
  `1987` int(5) DEFAULT NULL,
  `1988` int(5) DEFAULT NULL,
  `1989` int(5) DEFAULT NULL,
  `1990` int(5) DEFAULT NULL,
  `1991` int(5) DEFAULT NULL,
  `1992` int(5) DEFAULT NULL,
  `1993` int(5) DEFAULT NULL,
  `1994` int(5) DEFAULT NULL,
  `1995` int(5) DEFAULT NULL,
  `1996` int(5) DEFAULT NULL,
  `1997` int(5) DEFAULT NULL,
  `1998` int(5) DEFAULT NULL,
  `1999` int(5) DEFAULT NULL,
  `2000` int(5) DEFAULT NULL,
  `2001` int(5) DEFAULT NULL,
  `2002` int(5) DEFAULT NULL,
  `2003` int(5) DEFAULT NULL,
  `2004` int(5) DEFAULT NULL,
  `2005` int(5) DEFAULT NULL,
  `2006` int(5) DEFAULT NULL,
  `2007` int(5) DEFAULT NULL,
  `2008` int(5) DEFAULT NULL,
  `2009` int(5) DEFAULT NULL,
  `2010` int(5) DEFAULT NULL,
  `2011` int(5) DEFAULT NULL,
  `2012` int(5) DEFAULT NULL,
  `2013` int(5) DEFAULT NULL,
  `2014` int(5) DEFAULT NULL,
  `2015` int(5) DEFAULT NULL,
  `2016` int(5) DEFAULT NULL,
  `2017` int(5) DEFAULT NULL,
  `2018` int(5) DEFAULT NULL,
  `2019` int(5) DEFAULT NULL,
  `2020` int(5) DEFAULT NULL,
  `2021` int(5) DEFAULT NULL,
  `2022` int(5) DEFAULT NULL,
  `2023` int(5) DEFAULT NULL,
  `2024` int(5) DEFAULT NULL,
  `2025` int(5) DEFAULT NULL,
  `2026` int(5) DEFAULT NULL,
  `2027` int(5) DEFAULT NULL,
  `2028` int(5) DEFAULT NULL,
  `2029` int(5) DEFAULT NULL,
  `2030` int(5) DEFAULT NULL,
  `2031` int(5) DEFAULT NULL,
  `2032` int(5) DEFAULT NULL,
  `2033` int(5) DEFAULT NULL,
  `2034` int(5) DEFAULT NULL,
  `2035` int(5) DEFAULT NULL,
  `2036` int(5) DEFAULT NULL,
  `2037` int(5) DEFAULT NULL,
  `2038` int(5) DEFAULT NULL,
  PRIMARY KEY (`paper_id`),
  KEY `paper_id` (`paper_id`),
  CONSTRAINT `citations_ibfk_1` FOREIGN KEY (`paper_id`) REFERENCES `papers` (`paper_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `firstnames`
--

DROP TABLE IF EXISTS `firstnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firstnames` (
  `name` varchar(20) NOT NULL,
  `gender` char(7) DEFAULT NULL,
  `probability` float(3,2) DEFAULT NULL,
  `gender_fi` char(7) DEFAULT NULL,
  `probability_fi` float(3,2) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `papers`
--

DROP TABLE IF EXISTS `papers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `papers` (
  `paper_id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `thesis_id` varchar(68) DEFAULT NULL,
  `pubmed_id` int(11) DEFAULT NULL,
  `author` varchar(37) NOT NULL,
  `author_position` smallint(6) NOT NULL,
  `shared_for_thesis` tinyint(2) DEFAULT NULL,
  `status` tinyint(3) NOT NULL,
  `date` char(10) NOT NULL,
  `journal` varchar(100) DEFAULT NULL,
  `volume` varchar(10) DEFAULT NULL,
  `page_range_begin` varchar(10) DEFAULT NULL,
  `page_number` smallint(3) NOT NULL,
  `title` varchar(255) NOT NULL,
  `journal_IF` decimal(6,3) DEFAULT NULL,
  `citations_5y` mediumint(9) DEFAULT NULL,
  `openaccess` tinyint(3) DEFAULT NULL,
  `scopus_id` bigint(11) DEFAULT NULL,
  `wos_id` int(15) DEFAULT NULL,
  `remarks` text,
  `doi` varchar(64) DEFAULT NULL,
  `shared_for_publication` tinyint(2) DEFAULT NULL,
  `totalcitations` mediumint(9) DEFAULT NULL,
  `issn` int(8) DEFAULT NULL,
  `cited_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`paper_id`),
  KEY `thesis_id` (`thesis_id`),
  KEY `author` (`author`),
  CONSTRAINT `papers_ibfk_1` FOREIGN KEY (`thesis_id`) REFERENCES `thesis` (`id`),
  CONSTRAINT `papers_ibfk_2` FOREIGN KEY (`author`) REFERENCES `thesis` (`dccontributorauthorfi`)
) ENGINE=InnoDB AUTO_INCREMENT=795 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `theses`
--

DROP TABLE IF EXISTS `theses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `theses` (
  `melinda_id` int(10) NOT NULL,
  `author` varchar(255) NOT NULL,
  `title` varchar(767) DEFAULT NULL,
  `university` varchar(255) NOT NULL,
  `issn` varchar(18) DEFAULT NULL,
  `date` varchar(10) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `language` varchar(7) DEFAULT NULL,
  `gender` varchar(7) DEFAULT NULL,
  `fulltext_online` tinyint(1) DEFAULT NULL,
  `local_filename` varchar(255) DEFAULT NULL,
  `thesis_type` varchar(13) DEFAULT NULL,
  PRIMARY KEY (`melinda_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `thesis`
--

DROP TABLE IF EXISTS `thesis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `thesis` (
  `id` varchar(6) NOT NULL,
  `collection` varchar(24) DEFAULT NULL,
  `dcaccessrights` varchar(1) DEFAULT NULL,
  `dcaccrualmethodfi` varchar(2522) DEFAULT NULL,
  `dccontributorauthorfi` varchar(37) DEFAULT NULL,
  `dccontributoren` varchar(511) DEFAULT NULL,
  `dccontributorfi` varchar(274) DEFAULT NULL,
  `dccontributorsv` varchar(147) DEFAULT NULL,
  `dcdateissuedfi` date DEFAULT NULL,
  `dcdescriptionabstract` text,
  `dcdescriptionabstracten` text,
  `dcdescriptionabstractes` text,
  `dcdescriptionabstractfi` text,
  `dcdescriptionabstractfr` text,
  `dcdescriptionabstractnl` text,
  `dcdescriptionabstractru` text,
  `dcdescriptionabstractse` text,
  `dcdescriptionabstractsv` text,
  `dcdescriptionabstractsw` text,
  `dcdescriptionnote` varchar(42) DEFAULT NULL,
  `dcformatmimetypefi` varchar(15) DEFAULT NULL,
  `dcidentifierisbn` varchar(16) DEFAULT NULL,
  `dcidentifieruri` varchar(68) DEFAULT NULL,
  `dcidentifierurien` varchar(26) DEFAULT NULL,
  `dcidentifierurifi` varchar(33) DEFAULT NULL,
  `dclanguageisoen` varchar(2) DEFAULT NULL,
  `dclanguageisofi` varchar(6) DEFAULT NULL,
  `dcopnen` varchar(37) DEFAULT NULL,
  `dcopnfi` varchar(40) DEFAULT NULL,
  `dcpublisher` varchar(32) DEFAULT NULL,
  `dcpublisheren` varchar(22) DEFAULT NULL,
  `dcpublisherfi` varchar(204) DEFAULT NULL,
  `dcpublishersv` varchar(23) DEFAULT NULL,
  `dcrelationisformatof` varchar(26) DEFAULT NULL,
  `dcrelationisformatofen` varchar(169) DEFAULT NULL,
  `dcrelationisformatoffi` varchar(295) DEFAULT NULL,
  `dcrelationispartof` date DEFAULT NULL,
  `dcrelationispartofen` varchar(68) DEFAULT NULL,
  `dcrelationispartoffi` varchar(182) DEFAULT NULL,
  `dcrightsen` varchar(128) DEFAULT NULL,
  `dcrightsfi` varchar(154) DEFAULT NULL,
  `dcrightssv` varchar(138) DEFAULT NULL,
  `dcsubject` varchar(1) DEFAULT NULL,
  `dcsubjecten` varchar(23) DEFAULT NULL,
  `dcsubjectfi` varchar(84) DEFAULT NULL,
  `dcths` varchar(12) DEFAULT NULL,
  `dcthsen` varchar(31) DEFAULT NULL,
  `dcthsfi` varchar(97) DEFAULT NULL,
  `dctitle` varchar(148) DEFAULT NULL,
  `dctitlealternativeen` varchar(245) DEFAULT NULL,
  `dctitlealternativefi` varchar(285) DEFAULT NULL,
  `dctitlealternativesv` varchar(223) DEFAULT NULL,
  `dctitlede` varchar(220) DEFAULT NULL,
  `dctitleen` varchar(287) DEFAULT NULL,
  `dctitlees` varchar(183) DEFAULT NULL,
  `dctitlefi` varchar(242) DEFAULT NULL,
  `dctitlefr` varchar(142) DEFAULT NULL,
  `dctitlehu` varchar(113) DEFAULT NULL,
  `dctitleit` varchar(120) DEFAULT NULL,
  `dctitleother` varchar(86) DEFAULT NULL,
  `dctitleru` varchar(95) DEFAULT NULL,
  `dctitlesv` varchar(291) DEFAULT NULL,
  `dctypedcmitypeen` varchar(4) DEFAULT NULL,
  `dctypedcmitypefi` varchar(4) DEFAULT NULL,
  `dctypefi` varchar(9) DEFAULT NULL,
  `dctypeontasoten` varchar(37) DEFAULT NULL,
  `dctypeontasotfi` varchar(24) DEFAULT NULL,
  `dctypeontasotsv` varchar(34) DEFAULT NULL,
  `doriadoriaadditionalinfoen` varchar(61) DEFAULT NULL,
  `doriadoriaadditionalinfofi` varchar(75) DEFAULT NULL,
  `doriadoriaadditionalinfosv` varchar(64) DEFAULT NULL,
  `doriadoriasalesen` varchar(159) DEFAULT NULL,
  `doriadoriasalesfi` varchar(216) DEFAULT NULL,
  `doriadoriasalessv` varchar(136) DEFAULT NULL,
  `dcdateissued` char(10) DEFAULT NULL,
  `gender` varchar(7) DEFAULT NULL,
  `fulltext_online` tinyint(1) DEFAULT NULL,
  `local_filename` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dcidentifieruri` (`dcidentifieruri`),
  KEY `dccontributorauthorfi` (`dccontributorauthorfi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-02  6:39:22
