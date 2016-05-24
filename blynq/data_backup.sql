-- MySQL dump 10.13  Distrib 5.7.9, for osx10.10 (x86_64)
--
-- Host: localhost    Database: Blynq_DB_DEV
-- ------------------------------------------------------
-- Server version	5.7.9

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add city',7,'add_city'),(20,'Can change city',7,'change_city'),(21,'Can delete city',7,'delete_city'),(22,'Can add address',8,'add_address'),(23,'Can change address',8,'change_address'),(24,'Can delete address',8,'delete_address'),(25,'Can add organization',9,'add_organization'),(26,'Can change organization',9,'change_organization'),(27,'Can delete organization',9,'delete_organization'),(28,'Can add role',10,'add_role'),(29,'Can change role',10,'change_role'),(30,'Can delete role',10,'delete_role'),(31,'Can add user',11,'add_userdetails'),(32,'Can change user',11,'change_userdetails'),(33,'Can delete user',11,'delete_userdetails'),(34,'Can add screen status',12,'add_screenstatus'),(35,'Can change screen status',12,'change_screenstatus'),(36,'Can delete screen status',12,'delete_screenstatus'),(37,'Can add group',13,'add_group'),(38,'Can change group',13,'change_group'),(39,'Can delete group',13,'delete_group'),(40,'Can add screen specs',14,'add_screenspecs'),(41,'Can change screen specs',14,'change_screenspecs'),(42,'Can delete screen specs',14,'delete_screenspecs'),(43,'Can add screen',15,'add_screen'),(44,'Can change screen',15,'change_screen'),(45,'Can delete screen',15,'delete_screen'),(46,'Can add content type',16,'add_contenttype'),(47,'Can change content type',16,'change_contenttype'),(48,'Can delete content type',16,'delete_contenttype'),(49,'Can add content',17,'add_content'),(50,'Can change content',17,'change_content'),(51,'Can delete content',17,'delete_content'),(52,'Can add playlist items',18,'add_playlistitems'),(53,'Can change playlist items',18,'change_playlistitems'),(54,'Can delete playlist items',18,'delete_playlistitems'),(55,'Can add playlist',19,'add_playlist'),(56,'Can change playlist',19,'change_playlist'),(57,'Can delete playlist',19,'delete_playlist'),(61,'Can add schedule',21,'add_schedule'),(62,'Can change schedule',21,'change_schedule'),(63,'Can delete schedule',21,'delete_schedule'),(70,'Can add calendar',24,'add_calendar'),(71,'Can change calendar',24,'change_calendar'),(72,'Can delete calendar',24,'delete_calendar'),(73,'Can add calendar relation',25,'add_calendarrelation'),(74,'Can change calendar relation',25,'change_calendarrelation'),(75,'Can delete calendar relation',25,'delete_calendarrelation'),(76,'Can add rule',26,'add_rule'),(77,'Can change rule',26,'change_rule'),(78,'Can delete rule',26,'delete_rule'),(79,'Can add event',27,'add_event'),(80,'Can change event',27,'change_event'),(81,'Can delete event',27,'delete_event'),(82,'Can add event relation',28,'add_eventrelation'),(83,'Can change event relation',28,'change_eventrelation'),(84,'Can delete event relation',28,'delete_eventrelation'),(85,'Can add occurrence',29,'add_occurrence'),(86,'Can change occurrence',29,'change_occurrence'),(87,'Can delete occurrence',29,'delete_occurrence'),(100,'Can add requested quote',34,'add_requestedquote'),(101,'Can change requested quote',34,'change_requestedquote'),(102,'Can delete requested quote',34,'delete_requestedquote'),(103,'Can add schedule playlists',35,'add_scheduleplaylists'),(104,'Can change schedule playlists',35,'change_scheduleplaylists'),(105,'Can delete schedule playlists',35,'delete_scheduleplaylists'),(106,'Can add schedule screens',36,'add_schedulescreens'),(107,'Can change schedule screens',36,'change_schedulescreens'),(108,'Can delete schedule screens',36,'delete_schedulescreens'),(109,'Can add group screens',37,'add_groupscreens'),(110,'Can change group screens',37,'change_groupscreens'),(111,'Can delete group screens',37,'delete_groupscreens'),(112,'Can add revision',38,'add_revision'),(113,'Can change revision',38,'change_revision'),(114,'Can delete revision',38,'delete_revision'),(115,'Can add version',39,'add_version'),(116,'Can change version',39,'change_version'),(117,'Can delete version',39,'delete_version'),(118,'Can add screen activation key',40,'add_screenactivationkey'),(119,'Can change screen activation key',40,'change_screenactivationkey'),(120,'Can delete screen activation key',40,'delete_screenactivationkey');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$SqQofbBFt1mm$CsDDuv+oh4QcrJvMeadmQ+hiXsj6ofeBePlEgfEPU9s=','2016-05-17 07:06:59.878242',1,'admin','','','admin@gmail.com',1,1,'2016-04-22 06:32:39.913688'),(5,'pbkdf2_sha256$20000$5MobmJBtYQzj$ZXSERJnNNZ2AQbqewdHrPecqC2A2PLVu/SK6/rYp3t0=','2016-04-22 07:26:11.047069',0,'jaydev','jaydev','kalivarapu','jaydev@gmail.com',0,1,'2016-04-22 07:25:49.122709'),(7,'pbkdf2_sha256$20000$PUxTJLrDbayP$AHpHYc6EmoZrPrCoWKYEan9LxHF/lyzr+wtk2xUZC5M=','2016-04-22 11:11:54.410590',0,'blynq','blynq','technologies','blynq@gmail.com',0,1,'2016-04-22 11:11:38.974145'),(8,'pbkdf2_sha256$20000$Mv4AbkbrBl55$iWTc/A7Thc64f3uU5TifJJmVyZyZajadB5r1QsnKrEc=','2016-05-24 05:45:25.507189',0,'nipun','Nipun','Edara','nipun425@gmail.com',0,1,'2016-04-22 11:12:38.176576'),(9,'pbkdf2_sha256$20000$R0ktrto3ZsYb$sS27znxrpJPEmSZZXacdS6fx6Ekp0wA9LpiCWpdmUDE=','2016-04-22 11:15:34.224634',0,'kmpk123','prasanth','kuriseti','kmpk123@gmail.com',0,1,'2016-04-22 11:13:09.428652');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_address`
--

DROP TABLE IF EXISTS `authentication_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_address` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) NOT NULL,
  `address_line1` varchar(100) NOT NULL,
  `address_line2` varchar(100) NOT NULL,
  `area` varchar(100) NOT NULL,
  `landmark` varchar(100) NOT NULL,
  `pincode` int(11) NOT NULL,
  `added_by_id` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  PRIMARY KEY (`address_id`),
  UNIQUE KEY `authentication_address_building_name_307a710555774b15_uniq` (`building_name`,`added_by_id`),
  KEY `authentication_address_0c5d7d4e` (`added_by_id`),
  KEY `authentication_address_c7141997` (`city_id`),
  CONSTRAINT `D25140194e265ed788a324faa846663b` FOREIGN KEY (`added_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `authenti_city_id_392ccb660d3eb8f0_fk_authentication_city_city_id` FOREIGN KEY (`city_id`) REFERENCES `authentication_city` (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_address`
--

LOCK TABLES `authentication_address` WRITE;
/*!40000 ALTER TABLE `authentication_address` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_city`
--

DROP TABLE IF EXISTS `authentication_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_city`
--

LOCK TABLES `authentication_city` WRITE;
/*!40000 ALTER TABLE `authentication_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_organization`
--

DROP TABLE IF EXISTS `authentication_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_organization` (
  `organization_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `website` varchar(100) NOT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `total_file_size_limit` bigint(20) NOT NULL,
  `used_file_size` bigint(20) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_organization`
--

LOCK TABLES `authentication_organization` WRITE;
/*!40000 ALTER TABLE `authentication_organization` DISABLE KEYS */;
INSERT INTO `authentication_organization` VALUES (1,'Blynq Pvt Ltd','http://www.blynq.in','8277121319','Sastry house, pragathi nagar, hyderabad',5368709120,0),(2,'TestOrganization2','www.google.com','9440806969','sanath nagar, hyderabad',5368709120,0);
/*!40000 ALTER TABLE `authentication_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_requestedquote`
--

DROP TABLE IF EXISTS `authentication_requestedquote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_requestedquote` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `mobile_number` varchar(12) NOT NULL,
  `num_of_devices` int(11) NOT NULL,
  `additional_details` longtext,
  `requested_on` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_requestedquote`
--

LOCK TABLES `authentication_requestedquote` WRITE;
/*!40000 ALTER TABLE `authentication_requestedquote` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_requestedquote` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_role`
--

DROP TABLE IF EXISTS `authentication_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  `role_description` varchar(100) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_role`
--

LOCK TABLES `authentication_role` WRITE;
/*!40000 ALTER TABLE `authentication_role` DISABLE KEYS */;
INSERT INTO `authentication_role` VALUES (1,'viewer','User who can just view content and schedules.'),(2,'scheduler','User who can view as well as schedule content on the screens'),(3,'manager','User who can schedule+ modify user roles for that company');
/*!40000 ALTER TABLE `authentication_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_userdetails`
--

DROP TABLE IF EXISTS `authentication_userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_userdetails` (
  `user_ptr_id` int(11) NOT NULL,
  `mobile_number` varchar(12) NOT NULL,
  `organization_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`user_ptr_id`),
  KEY `f6a950242aa695a19cf9a8637c2378a7` (`organization_id`),
  KEY `authenti_role_id_44612207d2201d34_fk_authentication_role_role_id` (`role_id`),
  CONSTRAINT `authenti_role_id_44612207d2201d34_fk_authentication_role_role_id` FOREIGN KEY (`role_id`) REFERENCES `authentication_role` (`role_id`),
  CONSTRAINT `authentication_user_user_ptr_id_70f39c7da29ecb96_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `f6a950242aa695a19cf9a8637c2378a7` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_userdetails`
--

LOCK TABLES `authentication_userdetails` WRITE;
/*!40000 ALTER TABLE `authentication_userdetails` DISABLE KEYS */;
INSERT INTO `authentication_userdetails` VALUES (5,'1234567890',1,2),(7,'8277121319',1,3),(8,'+91827712131',1,2),(9,'1234567890',2,3);
/*!40000 ALTER TABLE `authentication_userdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contentManagement_content`
--

DROP TABLE IF EXISTS `contentManagement_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentManagement_content` (
  `content_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `document` varchar(100) DEFAULT NULL,
  `sha1_hash` varchar(40) NOT NULL,
  `original_filename` varchar(100) DEFAULT NULL,
  `uploaded_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `is_folder` tinyint(1) NOT NULL,
  `relative_path` varchar(1025) NOT NULL,
  `last_modified_by_id` int(11) NOT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `parent_folder_id` int(11) DEFAULT NULL,
  `uploaded_by_id` int(11) NOT NULL,
  `document_type` varchar(50) NOT NULL,
  PRIMARY KEY (`content_id`),
  KEY `contentManagement_content_7fa85557` (`last_modified_by_id`),
  KEY `contentManagement_content_26b2345e` (`organization_id`),
  KEY `contentManagement_content_ce25f862` (`parent_folder_id`),
  KEY `contentManagement_content_4095e96b` (`uploaded_by_id`),
  CONSTRAINT `D030273c9e61c272ad95472f688031ac` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `D4fefcd379e53b14288cdd718a20b7b5` FOREIGN KEY (`last_modified_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `a4652993b4665036cee91bc59709d44d` FOREIGN KEY (`uploaded_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `c28200b62fd5064ce5f884826faee3c7` FOREIGN KEY (`parent_folder_id`) REFERENCES `contentManagement_content` (`content_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_content`
--

LOCK TABLES `contentManagement_content` WRITE;
/*!40000 ALTER TABLE `contentManagement_content` DISABLE KEYS */;
INSERT INTO `contentManagement_content` VALUES (8,'Jaffa','','',NULL,'2016-04-24 14:38:49.933946','2016-04-24 14:38:49.934053',1,'/',8,1,NULL,8,''),(21,'inside jaffa','','',NULL,'2016-04-25 06:00:56.622113','2016-04-25 06:00:56.622163',1,'/',8,1,8,8,''),(22,'logo','usercontent/8/blynq_logo.png','',NULL,'2016-04-25 06:01:21.569886','2016-04-25 06:01:21.569967',0,'/',8,1,8,8,''),(23,'groups ui','usercontent/8/Groups UI.png','',NULL,'2016-04-25 09:24:32.045743','2016-04-25 09:24:32.045812',0,'/',8,1,8,8,''),(24,'logo','usercontent/8/blynq_logo_YZWVlEC.png','',NULL,'2016-04-26 10:00:36.175680','2016-04-26 10:00:36.175751',0,'/',8,1,NULL,8,''),(25,'sastry','','',NULL,'2016-05-04 12:14:44.069166','2016-05-04 12:14:44.069287',1,'/',8,1,NULL,8,''),(26,'Flow diagram','usercontent/8/flow_diagram.jpg','',NULL,'2016-05-04 12:15:08.194831','2016-05-04 12:15:08.194897',0,'/',8,1,25,8,'');
/*!40000 ALTER TABLE `contentManagement_content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contentManagement_contenttype`
--

DROP TABLE IF EXISTS `contentManagement_contenttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentManagement_contenttype` (
  `content_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(3) NOT NULL,
  `file_extension` varchar(10) NOT NULL,
  PRIMARY KEY (`content_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_contenttype`
--

LOCK TABLES `contentManagement_contenttype` WRITE;
/*!40000 ALTER TABLE `contentManagement_contenttype` DISABLE KEYS */;
/*!40000 ALTER TABLE `contentManagement_contenttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-04-22 06:35:31.975476','1','Blynq Pvt Ltd',1,'',9,1),(2,'2016-04-22 06:36:11.974841','2','TestOrganization2',1,'',9,1),(3,'2016-04-22 06:38:52.231767','1','viewer',1,'',10,1),(4,'2016-04-22 06:40:11.592123','2','scheduler',1,'',10,1),(5,'2016-04-22 06:40:28.895113','3','manager',1,'',10,1),(6,'2016-04-22 06:41:33.028602','2','blynq',1,'',11,1),(7,'2016-04-22 06:42:18.224503','3','nipun',1,'',11,1),(8,'2016-04-22 06:44:44.936902','4','kmpk123',1,'',11,1),(9,'2016-04-22 06:45:48.884127','1','bangalore 1',1,'',13,1),(10,'2016-04-22 06:46:07.432807','2','bangalore 2',1,'',13,1),(11,'2016-04-22 06:46:49.857408','3','hyderabad 1',1,'',13,1),(12,'2016-04-22 06:47:12.344962','4','hyderabad 2',1,'',13,1),(13,'2016-04-22 06:48:20.261650','1','Unactivated',1,'',12,1),(14,'2016-04-22 06:49:05.785756','2','Online',1,'',12,1),(15,'2016-04-22 06:49:27.786467','3','Offline',1,'',12,1),(16,'2016-04-22 06:50:10.900914','4','Idle',1,'',12,1),(17,'2016-04-22 06:52:30.969449','1','bellandur 1',1,'',15,1),(18,'2016-04-22 06:53:44.641054','2','screen 2',1,'',15,1),(19,'2016-04-22 06:55:29.817983','3','hyd orbit 1',1,'',15,1),(20,'2016-04-22 06:56:23.957961','4','hyd orbit 2',1,'',15,1),(21,'2016-04-22 07:45:55.555679','1','bangalore 1',2,'Changed created_by.',13,1),(22,'2016-04-22 07:46:02.105668','2','bangalore 2',2,'Changed created_by.',13,1),(23,'2016-04-22 07:46:08.198043','3','hyderabad 1',2,'Changed created_by.',13,1),(24,'2016-04-22 07:46:14.458728','4','hyderabad 2',2,'Changed created_by.',13,1),(25,'2016-04-22 07:46:40.090793','4','hyd orbit 2',2,'Changed activated_by.',15,1),(26,'2016-04-22 07:46:47.868025','3','hyd orbit 1',2,'Changed activated_by.',15,1),(27,'2016-04-22 07:46:55.836043','2','screen 2',2,'Changed activated_by.',15,1),(28,'2016-04-22 07:47:02.991106','1','bellandur 1',2,'Changed activated_by.',15,1),(29,'2016-04-22 07:50:32.715096','6','sastry',1,'',4,1),(30,'2016-04-22 11:10:18.408622','2','blynq',3,'',4,1),(31,'2016-04-22 11:10:18.416316','4','kmpk123',3,'',4,1),(32,'2016-04-22 11:10:18.420189','3','nipun',3,'',4,1),(33,'2016-04-22 11:10:18.428245','6','sastry',3,'',4,1),(34,'2016-04-22 11:14:09.474238','1','bangalore 1',2,'Changed created_by.',13,1),(35,'2016-04-22 11:14:16.915189','1','bangalore 1',2,'Changed created_by.',13,1),(36,'2016-04-22 11:14:23.466001','2','bangalore 2',2,'Changed created_by.',13,1),(37,'2016-04-22 11:14:28.964783','3','hyderabad 1',2,'Changed created_by.',13,1),(38,'2016-04-22 11:14:34.116173','4','hyderabad 2',2,'Changed created_by.',13,1),(39,'2016-04-22 11:14:46.390893','2','screen 2',2,'Changed activated_by.',15,1),(40,'2016-04-22 11:14:52.282249','1','bellandur 1',2,'Changed activated_by.',15,1),(41,'2016-04-22 11:14:58.780257','4','hyd orbit 2',2,'Changed activated_by.',15,1),(42,'2016-04-22 11:15:12.617404','3','hyd orbit 1',2,'Changed activated_by.',15,1),(43,'2016-04-25 05:32:31.637159','1','bangalore 1',2,'Changed organization.',13,1),(44,'2016-04-25 05:32:37.949614','2','bangalore 2',2,'Changed organization.',13,1),(45,'2016-04-25 05:32:44.412702','3','hyderabad 1',2,'Changed organization.',13,1),(46,'2016-04-25 05:32:50.838333','4','hyderabad 2',2,'Changed organization.',13,1),(47,'2016-04-25 10:24:28.670243','1','Playlist object',1,'',19,1),(48,'2016-04-25 10:26:58.223219','1','PlaylistItems object',1,'',18,1),(49,'2016-04-25 10:27:09.348365','2','PlaylistItems object',1,'',18,1),(50,'2016-04-26 06:12:21.567326','3','First playlist - inside jaffa',1,'',18,1),(51,'2016-04-27 09:56:01.313080','1','Flipkart Calendar',1,'',24,1),(52,'2016-04-27 09:56:35.207152','1','Rule Month start sale params ',1,'',26,1),(53,'2016-04-27 10:00:28.490568','1','Flipkart start month event: May 1, 2016 - June 1, 2016',1,'',27,1),(54,'2016-04-27 10:00:50.214390','1','Flipkart start month event: May 1, 2016 - May 1, 2016',2,'Changed end.',27,1),(55,'2016-04-27 10:01:30.751114','1','Flipkart Calendar - None',1,'',25,1),(56,'2016-04-28 02:29:09.170245','2','amazon calendar',1,'',24,1),(57,'2016-04-28 02:30:52.379897','2','Schedule one day two hours amazon event : April 28, 2016 - April 29, 2016',1,'',27,1),(58,'2016-04-28 03:01:11.311653','1','Schedule object',1,'',21,1),(59,'2016-04-28 03:01:39.012086','1','bellandur 1',2,'Changed screen_calendar.',15,1),(67,'2016-04-28 03:43:45.721461','2','Schedule one day two hours amazon event : April 28, 2016 - April 29, 2016',2,'Changed calendar.',27,1),(68,'2016-04-28 10:39:44.250950','1','First schedule',2,'Changed organization.',21,1),(69,'2016-04-28 10:39:49.965905','1','First schedule',2,'No fields changed.',21,1),(72,'2016-04-28 12:25:15.090974','2','Rule Daily params ',1,'',26,1),(74,'2016-05-07 14:37:13.976214','1','Flipkart start day event: May 1, 2016 - May 1, 2016',2,'Changed title, description and rule.',27,1),(77,'2016-05-10 17:46:23.108012','3','Rule Every monday, tuesday fortnight params \"interval:2;bysetpos:1,2\"',1,'',26,1),(78,'2016-05-10 18:20:20.584281','3','Every alternate monday, tuesday: May 8, 2016 - June 10, 2016',1,'',27,1),(79,'2016-05-11 01:47:13.711280','3','Every alternate monday, tuesday: May 8, 2016 - June 8, 2016',2,'Changed start and end.',27,1),(80,'2016-05-11 01:48:24.680484','3','Every alternate monday, tuesday: May 8, 2016 - May 8, 2016',2,'Changed end.',27,1),(81,'2016-05-11 01:52:45.314328','3','Rule Every monday, tuesday fortnight params interval:3',2,'Changed params.',26,1),(82,'2016-05-11 01:53:29.925122','3','Rule Every monday, tuesday fortnight params interval:5',2,'Changed params.',26,1),(83,'2016-05-11 01:58:51.548582','3','Rule Every monday, tuesday fortnight params interval:5;bysetpos:1,2,3',2,'Changed params.',26,1),(84,'2016-05-11 02:40:43.967305','3','Rule Every monday, tuesday fortnight params ',2,'Changed frequency and params.',26,1),(85,'2016-05-11 02:42:43.461741','3','Rule Every monday, tuesday fortnight params interval:3',2,'Changed params.',26,1),(86,'2016-05-11 02:52:40.425088','4','Rule Daily params ',1,'',26,1),(87,'2016-05-11 02:52:55.935697','2','Rule Daily params ',3,'',26,1),(88,'2016-05-11 02:53:39.069194','4','Rule blynq-Daily params ',2,'Changed name.',26,1),(89,'2016-05-11 02:54:23.730402','5','Rule blynq-weekly params ',1,'',26,1),(90,'2016-05-11 02:54:59.558116','6','Rule default-yearly params ',1,'',26,1),(91,'2016-05-11 02:55:09.071820','5','Rule default-weekly params ',2,'Changed name.',26,1),(92,'2016-05-11 02:55:21.198659','4','Rule default-Daily params ',2,'Changed name.',26,1),(93,'2016-05-11 02:55:33.255437','4','Rule default-daily params ',2,'Changed name.',26,1),(94,'2016-05-11 03:19:58.370256','6','Rule default-yearly params ',2,'No fields changed.',26,1),(95,'2016-05-11 03:20:27.819075','8','Rule default-monthly params ',1,'',26,1),(96,'2016-05-11 03:20:44.209291','7','Rule test params interval:3',3,'',26,1),(97,'2016-05-11 04:50:58.938752','1','First schedule-First playlist',1,'',35,1),(98,'2016-05-11 04:51:07.106423','2','First schedule-playlist 2',1,'',35,1),(99,'2016-05-11 04:51:49.803531','1','First schedule-bellandur 1',1,'',36,1),(100,'2016-05-11 04:52:06.951295','2','First schedule-screen 2',1,'',36,1),(101,'2016-05-11 06:57:14.143973','3','Every alternate monday, tuesday: May 8, 2016 - May 8, 2016',2,'Changed end_recurring_period.',27,1),(102,'2016-05-11 06:59:31.237326','2','Schedule one day two hours amazon event : April 28, 2016 - April 28, 2016',2,'Changed end and end_recurring_period.',27,1),(103,'2016-05-13 19:29:16.587152','2','new schedule',1,'',21,1),(104,'2016-05-13 19:30:07.663016','3','new schedule-bellandur 1',1,'',36,1),(105,'2016-05-13 19:30:07.895828','4','new schedule-bellandur 1',1,'',36,1),(106,'2016-05-13 19:30:42.254988','3','new schedule-abc',1,'',35,1),(107,'2016-05-14 07:44:50.541460','4','Full day event: May 14, 2016 - May 14, 2016',1,'',27,1),(108,'2016-05-14 07:45:30.740479','4','new schedule-bellandur 1',2,'Changed event.',36,1),(109,'2016-05-14 07:46:14.254716','3','new schedule-First playlist',2,'Changed playlist.',35,1),(110,'2016-05-14 12:06:33.297043','3','new schedule-bellandur 1',3,'',36,1),(111,'2016-05-14 12:06:54.020341','2','First schedule-screen 2',2,'Changed event.',36,1),(112,'2016-05-14 12:10:08.884474','4','new schedule-bellandur 1',2,'No fields changed.',36,1),(113,'2016-05-14 12:10:15.709157','1','First schedule-bellandur 1',2,'Changed event.',36,1),(114,'2016-05-17 10:05:17.566114','5','empty group',2,'Changed organization.',13,1),(115,'2016-05-18 03:43:29.996693','36','test schedule 1 - screen hyd orbit 1 - group hyderabad 1',1,'',36,1),(116,'2016-05-18 03:43:56.758614','36','test schedule 1 - screen hyd orbit 1 - group hyderabad 1',3,'',36,1),(117,'2016-05-18 03:44:38.319148','35','test schedule 1 - screen bellandur 1 - group empty group',2,'Changed screen.',36,1),(118,'2016-05-18 03:45:10.171032','35','test schedule 1 - group empty group',2,'Changed screen.',36,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(8,'authentication','address'),(7,'authentication','city'),(9,'authentication','organization'),(34,'authentication','requestedquote'),(10,'authentication','role'),(11,'authentication','userdetails'),(17,'contentManagement','content'),(16,'contentManagement','contenttype'),(5,'contenttypes','contenttype'),(19,'playlistManagement','playlist'),(18,'playlistManagement','playlistitems'),(38,'reversion','revision'),(39,'reversion','version'),(24,'schedule','calendar'),(25,'schedule','calendarrelation'),(27,'schedule','event'),(28,'schedule','eventrelation'),(29,'schedule','occurrence'),(26,'schedule','rule'),(21,'scheduleManagement','schedule'),(35,'scheduleManagement','scheduleplaylists'),(36,'scheduleManagement','schedulescreens'),(13,'screenManagement','group'),(37,'screenManagement','groupscreens'),(15,'screenManagement','screen'),(40,'screenManagement','screenactivationkey'),(14,'screenManagement','screenspecs'),(12,'screenManagement','screenstatus'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-04-22 06:14:27.142432'),(2,'auth','0001_initial','2016-04-22 06:14:27.672152'),(3,'admin','0001_initial','2016-04-22 06:14:27.799562'),(4,'contenttypes','0002_remove_content_type_name','2016-04-22 06:14:27.953275'),(5,'auth','0002_alter_permission_name_max_length','2016-04-22 06:14:28.012227'),(6,'auth','0003_alter_user_email_max_length','2016-04-22 06:14:28.064646'),(7,'auth','0004_alter_user_username_opts','2016-04-22 06:14:28.082069'),(8,'auth','0005_alter_user_last_login_null','2016-04-22 06:14:28.146214'),(9,'auth','0006_require_contenttypes_0002','2016-04-22 06:14:28.152336'),(10,'authentication','0001_initial','2016-04-22 06:14:28.896733'),(11,'contentManagement','0001_initial','2016-04-22 06:14:29.782199'),(12,'playlistManagement','0001_initial','2016-04-22 06:14:30.174308'),(13,'screenManagement','0001_initial','2016-04-22 06:14:30.803252'),(14,'scheduleManagement','0001_initial','2016-04-22 06:14:31.419035'),(15,'sessions','0001_initial','2016-04-22 06:14:31.478635'),(16,'authentication','0002_auto_20160422_0634','2016-04-22 06:34:45.369440'),(17,'contentManagement','0002_remove_content_description','2016-04-22 19:14:20.995266'),(18,'playlistManagement','0002_auto_20160422_1914','2016-04-22 19:14:21.061820'),(19,'contentManagement','0002_auto_20160424_1514','2016-04-24 15:14:37.319927'),(20,'screenManagement','0002_group_organization','2016-04-25 05:31:29.419374'),(21,'playlistManagement','0002_auto_20160425_2051','2016-04-25 20:51:22.815014'),(22,'playlistManagement','0002_auto_20160426_0714','2016-04-26 07:14:45.794458'),(23,'scheduleManagement','0002_auto_20160427_0640','2016-04-27 06:41:06.625644'),(24,'schedule','0001_initial','2016-04-27 09:51:37.178588'),(25,'scheduleManagement','0003_auto_20160427_2018','2016-04-27 14:49:05.238717'),(26,'screenManagement','0002_screen_screen_calendar','2016-04-28 02:25:39.012409'),(27,'scheduleManagement','0002_auto_20160428_0822','2016-04-28 02:57:00.912806'),(28,'scheduleManagement','0003_remove_schedule_event','2016-04-28 02:59:14.975272'),(29,'scheduleManagement','0004_schedule_event','2016-04-28 02:59:50.402020'),(30,'scheduleManagement','0005_auto_20160428_0836','2016-04-28 03:06:30.044059'),(31,'scheduleManagement','0006_auto_20160428_0836','2016-04-28 03:06:50.243485'),(32,'scheduleManagement','0007_auto_20160428_0837','2016-04-28 03:07:55.654473'),(33,'scheduleManagement','0008_auto_20160428_1038','2016-04-28 10:38:26.807356'),(34,'playlistManagement','0002_auto_20160429_1503','2016-04-29 15:03:07.017994'),(35,'scheduleManagement','0002_auto_20160429_1516','2016-04-29 17:36:45.984785'),(36,'scheduleManagement','0002_auto_20160429_1838','2016-04-29 18:41:16.661900'),(37,'scheduleManagement','0002_auto_20160429_1852','2016-04-29 18:53:00.054649'),(38,'scheduleManagement','0003_screenschedule_group','2016-04-29 18:53:36.158906'),(39,'scheduleManagement','0004_screenschedule_created_by','2016-04-29 18:53:59.180038'),(40,'scheduleManagement','0005_auto_20160429_1855','2016-04-29 18:55:34.327062'),(41,'scheduleManagement','0002_auto_20160429_1857','2016-04-29 18:58:06.114352'),(42,'scheduleManagement','0003_auto_20160429_1858','2016-04-29 18:59:26.536372'),(43,'scheduleManagement','0004_auto_20160429_1859','2016-04-29 19:00:22.193849'),(44,'screenManagement','0002_auto_20160429_1903','2016-04-29 19:04:14.625108'),(45,'screenManagement','0003_auto_20160429_1909','2016-04-29 19:09:38.995705'),(46,'screenManagement','0004_auto_20160429_1910','2016-04-29 19:10:29.832800'),(47,'scheduleManagement','0002_auto_20160429_1911','2016-04-29 19:11:49.484390'),(48,'scheduleManagement','0002_auto_20160429_1913','2016-04-29 19:14:01.536206'),(49,'scheduleManagement','0002_auto_20160429_1917','2016-04-29 19:17:52.487696'),(50,'screenManagement','0002_auto_20160429_1917','2016-04-29 19:17:52.497695'),(51,'screenManagement','0003_screengroups','2016-04-29 19:18:28.777324'),(52,'screenManagement','0004_screen_groups','2016-04-29 19:18:58.879393'),(53,'scheduleManagement','0003_auto_20160430_1422','2016-04-30 14:23:00.595909'),(54,'schedule','0002_event_color_event','2016-05-05 07:16:30.305460'),(55,'playlistManagement','0002_playlist_playlist_total_time','2016-05-07 12:21:34.835259'),(56,'scheduleManagement','0004_auto_20160507_1228','2016-05-07 12:28:50.037410'),(57,'scheduleManagement','0005_auto_20160507_1357','2016-05-07 13:57:32.314665'),(58,'screenManagement','0005_auto_20160509_0605','2016-05-09 06:05:12.117198'),(59,'scheduleManagement','0002_auto_20160510_0420','2016-05-10 04:21:07.736648'),(60,'scheduleManagement','0002_auto_20160510_0422','2016-05-10 04:22:52.968493'),(61,'authentication','0002_remove_organization_total_file_size_limit','2016-05-10 04:24:47.174609'),(62,'authentication','0003_organization_total_file_size_limit','2016-05-10 04:27:30.012546'),(63,'authentication','0004_remove_organization_total_file_size_limit','2016-05-10 04:27:30.019693'),(64,'scheduleManagement','0002_auto_20160510_0445','2016-05-10 04:45:17.765584'),(65,'scheduleManagement','0002_auto_20160510_0452','2016-05-10 04:53:16.658682'),(66,'authentication','0002_auto_20160510_0453','2016-05-10 04:53:42.630502'),(67,'authentication','0003_auto_20160510_0908','2016-05-10 09:09:01.977671'),(68,'scheduleManagement','0003_auto_20160510_0908','2016-05-10 09:09:02.846125'),(69,'scheduleManagement','0004_auto_20160510_0925','2016-05-10 09:26:03.622905'),(70,'scheduleManagement','0005_auto_20160510_0936','2016-05-10 09:38:00.277302'),(71,'scheduleManagement','0006_auto_20160510_0937','2016-05-10 09:38:00.393615'),(72,'scheduleManagement','0002_auto_20160510_1801','2016-05-10 18:02:36.005400'),(73,'scheduleManagement','0002_auto_20160510_1816','2016-05-11 04:44:20.951647'),(74,'scheduleManagement','0003_auto_20160511_0731','2016-05-11 07:32:00.185096'),(75,'scheduleManagement','0004_auto_20160511_1443','2016-05-11 14:44:40.880903'),(76,'scheduleManagement','0005_schedule_all_day','2016-05-13 19:28:39.648024'),(77,'contentManagement','0002_auto_20160516_1433','2016-05-16 14:33:10.213773'),(78,'screenManagement','0002_screengroups_created_by','2016-05-17 12:23:40.352604'),(79,'screenManagement','0003_auto_20160517_1236','2016-05-17 12:36:58.379497'),(80,'reversion','0001_initial','2016-05-18 02:15:11.422953'),(81,'reversion','0002_auto_20141216_1509','2016-05-18 02:15:11.529814'),(82,'contentManagement','0003_auto_20160518_0523','2016-05-18 05:23:48.315028'),(83,'contentManagement','0004_auto_20160518_0523','2016-05-18 05:23:48.418598'),(84,'contentManagement','0005_auto_20160518_0524','2016-05-18 05:24:55.982317'),(85,'scheduleManagement','0002_auto_20160523_1329','2016-05-23 13:54:17.991923'),(86,'screenManagement','0002_auto_20160523_1344','2016-05-23 13:54:18.010586'),(87,'screenManagement','0003_auto_20160523_1348','2016-05-23 13:54:18.022704'),(88,'screenManagement','0004_auto_20160523_1354','2016-05-23 13:54:18.029736'),(89,'screenManagement','0005_auto_20160523_1354','2016-05-23 13:54:47.837692'),(90,'screenManagement','0006_remove_screen_activation_key','2016-05-23 13:57:57.759737'),(91,'screenManagement','0007_screen_activation_key','2016-05-23 14:02:10.919319'),(92,'screenManagement','0008_auto_20160523_1453','2016-05-23 14:53:37.503142'),(93,'scheduleManagement','0003_auto_20160523_1502','2016-05-23 15:02:56.651825'),(94,'screenManagement','0009_auto_20160523_1509','2016-05-23 15:09:32.331859'),(95,'authentication','0002_auto_20160519_0848','2016-05-24 05:43:44.450791'),(96,'scheduleManagement','0006_auto_20160519_0848','2016-05-24 05:43:44.698465'),(97,'scheduleManagement','0007_merge','2016-05-24 05:43:44.703986'),(98,'screenManagement','0010_merge','2016-05-24 05:43:44.715770');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1aapdsylvi2kuxvi2zvr50lcgnovm23a','NGUyMDdiZWQ2ZDRjZjEyZTc5MGMyYTExN2E5ZTc0ZjJlZDg2NmQ2Nzp7Il9hdXRoX3VzZXJfaGFzaCI6IjE2ZGYzMzU5Mjk1ZGQ3Y2JlOTU5MmEwYmRmNzg1NDE3ZDQwYzcwYzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI4In0=','2016-06-07 05:45:25.520330'),('903z50kuzlw05o0ub5ndv5x6e23nlwu3','NGUyMDdiZWQ2ZDRjZjEyZTc5MGMyYTExN2E5ZTc0ZjJlZDg2NmQ2Nzp7Il9hdXRoX3VzZXJfaGFzaCI6IjE2ZGYzMzU5Mjk1ZGQ3Y2JlOTU5MmEwYmRmNzg1NDE3ZDQwYzcwYzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI4In0=','2016-05-31 07:02:12.842811'),('eop1u3nl0nt52qu2lhpb91ineee7i8tp','NGUyMDdiZWQ2ZDRjZjEyZTc5MGMyYTExN2E5ZTc0ZjJlZDg2NmQ2Nzp7Il9hdXRoX3VzZXJfaGFzaCI6IjE2ZGYzMzU5Mjk1ZGQ3Y2JlOTU5MmEwYmRmNzg1NDE3ZDQwYzcwYzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI4In0=','2016-05-29 05:48:59.969107'),('pi1vmcf2n7vzl93q0a0uxbubn17ysu6b','ODVmNjc2ZjhmYTU0NjIxMmZmZDcwZDEyNTkyNTA2OTc3YjMxNjRmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3MjhmMDBiZWUzN2JmNjNlYjIyOWNmNTgxMTRlOTc3Y2NjMGI4NzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-30 14:34:01.063753'),('rkss4d7rhtouzn83sfje1o9wm5f0vfqt','ODVmNjc2ZjhmYTU0NjIxMmZmZDcwZDEyNTkyNTA2OTc3YjMxNjRmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3MjhmMDBiZWUzN2JmNjNlYjIyOWNmNTgxMTRlOTc3Y2NjMGI4NzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-25 06:56:27.867699'),('uxf41czczacwmxycii2utewavs1m9q5k','ODVmNjc2ZjhmYTU0NjIxMmZmZDcwZDEyNTkyNTA2OTc3YjMxNjRmNjp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk3MjhmMDBiZWUzN2JmNjNlYjIyOWNmNTgxMTRlOTc3Y2NjMGI4NzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-05-31 07:06:59.893854');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlistManagement_playlist`
--

DROP TABLE IF EXISTS `playlistManagement_playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlistManagement_playlist` (
  `playlist_id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_title` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `last_updated_by_id` int(11) NOT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `playlist_total_time` int(11) NOT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `D50229839cd0cf7d84abc44588a9db0d` (`created_by_id`),
  KEY `c98e25b8402d78f8544a252ae221ba89` (`last_updated_by_id`),
  KEY `D9f916f791b6ae8d4fd6a9f347b63d4b` (`organization_id`),
  CONSTRAINT `D50229839cd0cf7d84abc44588a9db0d` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `D9f916f791b6ae8d4fd6a9f347b63d4b` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `c98e25b8402d78f8544a252ae221ba89` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlist`
--

LOCK TABLES `playlistManagement_playlist` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlist` DISABLE KEYS */;
INSERT INTO `playlistManagement_playlist` VALUES (1,'First playlist','2016-04-25 10:24:28.654764','2016-05-04 13:50:47.486028',8,8,1,0),(2,'abc','2016-04-26 10:28:37.589518','2016-04-26 10:28:37.593203',8,8,1,0),(4,'abc','2016-04-26 10:30:16.398610','2016-04-26 10:30:16.399392',8,8,1,0),(5,'playlist 2','2016-04-26 10:30:42.048235','2016-04-26 10:30:42.048332',8,8,1,0),(6,'xyz','2016-05-04 12:17:48.785768','2016-05-04 12:18:29.089376',8,8,1,0);
/*!40000 ALTER TABLE `playlistManagement_playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlistManagement_playlistitems`
--

DROP TABLE IF EXISTS `playlistManagement_playlistitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlistManagement_playlistitems` (
  `playlist_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `position_index` int(11) NOT NULL,
  `display_time` int(11) NOT NULL,
  `content_id` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  PRIMARY KEY (`playlist_item_id`),
  KEY `a5995af3c9ed21aaf6196289c9204d16` (`content_id`),
  KEY `D6f7b6973df14ff8936bc055e5fdcc7f` (`playlist_id`),
  CONSTRAINT `D6f7b6973df14ff8936bc055e5fdcc7f` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`playlist_id`),
  CONSTRAINT `a5995af3c9ed21aaf6196289c9204d16` FOREIGN KEY (`content_id`) REFERENCES `contentManagement_content` (`content_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlistitems`
--

LOCK TABLES `playlistManagement_playlistitems` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlistitems` DISABLE KEYS */;
INSERT INTO `playlistManagement_playlistitems` VALUES (2,2,10,23,1),(3,3,10,21,1),(4,1,15,22,1),(5,0,15,23,1),(6,0,15,26,6);
/*!40000 ALTER TABLE `playlistManagement_playlistitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reversion_revision`
--

DROP TABLE IF EXISTS `reversion_revision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reversion_revision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `manager_slug` varchar(191) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `comment` longtext NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reversion_revision_user_id_53d027e45b2ec55e_fk_auth_user_id` (`user_id`),
  KEY `reversion_revision_b16b0f06` (`manager_slug`),
  KEY `reversion_revision_c69e55a4` (`date_created`),
  CONSTRAINT `reversion_revision_user_id_53d027e45b2ec55e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_revision`
--

LOCK TABLES `reversion_revision` WRITE;
/*!40000 ALTER TABLE `reversion_revision` DISABLE KEYS */;
INSERT INTO `reversion_revision` VALUES (1,'default','2016-05-18 02:42:55.937639','Initial version.',NULL),(2,'default','2016-05-18 02:42:55.977002','Initial version.',NULL),(3,'default','2016-05-18 02:42:56.004975','Initial version.',NULL),(4,'default','2016-05-18 02:42:56.010868','Initial version.',NULL),(5,'default','2016-05-18 02:42:56.019240','Initial version.',NULL),(6,'default','2016-05-18 02:42:56.022970','Initial version.',NULL),(7,'default','2016-05-18 02:42:56.027890','Initial version.',NULL),(8,'default','2016-05-18 02:42:56.032438','Initial version.',NULL),(9,'default','2016-05-18 02:42:56.070208','Initial version.',NULL),(10,'default','2016-05-18 02:42:56.081095','Initial version.',NULL),(11,'default','2016-05-18 02:42:56.115212','Initial version.',NULL),(12,'default','2016-05-18 02:42:56.121867','Initial version.',NULL),(13,'default','2016-05-18 02:42:56.135582','Initial version.',NULL),(14,'default','2016-05-18 02:42:56.144961','Initial version.',NULL),(15,'default','2016-05-18 02:42:56.152317','Initial version.',NULL),(16,'default','2016-05-18 02:42:56.191157','Initial version.',NULL),(17,'default','2016-05-18 02:42:56.197881','Initial version.',NULL),(18,'default','2016-05-18 02:42:56.204881','Initial version.',NULL),(19,'default','2016-05-18 02:42:56.211515','Initial version.',NULL),(20,'default','2016-05-18 02:42:56.222990','Initial version.',NULL),(21,'default','2016-05-18 02:42:56.228839','Initial version.',NULL),(22,'default','2016-05-18 02:42:56.238395','Initial version.',NULL),(23,'default','2016-05-18 02:42:56.272511','Initial version.',NULL),(24,'default','2016-05-18 02:42:56.283615','Initial version.',NULL),(25,'default','2016-05-18 02:42:56.295048','Initial version.',NULL),(26,'default','2016-05-18 02:42:56.306215','Initial version.',NULL),(27,'default','2016-05-18 02:42:56.328126','Initial version.',NULL),(28,'default','2016-05-18 02:42:56.352348','Initial version.',NULL),(29,'default','2016-05-18 02:42:56.358741','Initial version.',NULL),(30,'default','2016-05-18 02:42:56.366012','Initial version.',NULL),(31,'default','2016-05-18 02:42:56.372450','Initial version.',NULL),(32,'default','2016-05-18 02:42:56.379766','Initial version.',NULL),(33,'default','2016-05-18 02:42:56.405270','Initial version.',NULL),(34,'default','2016-05-18 02:42:56.419687','Initial version.',NULL),(35,'default','2016-05-18 02:42:56.449538','Initial version.',NULL),(36,'default','2016-05-18 02:42:56.463612','Initial version.',NULL),(37,'default','2016-05-18 02:42:56.474447','Initial version.',NULL),(38,'default','2016-05-18 02:42:56.492315','Initial version.',NULL),(39,'default','2016-05-18 02:42:56.498765','Initial version.',NULL),(40,'default','2016-05-18 03:43:30.257498','Initial version.',1),(41,'default','2016-05-18 03:44:08.607126','',1),(42,'default','2016-05-18 03:44:38.334048','Changed screen.',1),(43,'default','2016-05-18 03:45:10.183483','Changed screen.',1),(44,'default','2016-05-18 03:45:21.837006','',1),(45,'default','2016-05-18 03:45:24.557094','',1),(46,'default','2016-05-18 03:45:30.403233','',1),(47,'default','2016-05-18 03:49:50.728903','Initial version.',NULL),(48,'default','2016-05-18 03:49:50.748767','Initial version.',NULL),(49,'default','2016-05-18 03:49:50.761465','Initial version.',NULL),(50,'default','2016-05-18 03:49:50.790403','Initial version.',NULL),(51,'default','2016-05-18 03:49:50.808016','Initial version.',NULL),(52,'default','2016-05-18 03:49:50.869134','Initial version.',NULL),(53,'default','2016-05-18 03:49:50.907971','Initial version.',NULL),(54,'default','2016-05-18 03:49:50.920826','Initial version.',NULL),(55,'default','2016-05-18 03:49:50.934908','Initial version.',NULL),(56,'default','2016-05-24 05:45:03.429417','',8),(57,'default','2016-05-24 05:45:25.544905','',8),(58,'default','2016-05-24 09:36:43.331867','',8),(59,'default','2016-05-24 09:38:06.723107','',8),(60,'default','2016-05-24 09:38:10.490073','',8),(61,'default','2016-05-24 10:44:19.525741','',8),(62,'default','2016-05-24 10:44:47.694759','',8),(63,'default','2016-05-24 10:45:00.984428','',8);
/*!40000 ALTER TABLE `reversion_revision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reversion_version`
--

DROP TABLE IF EXISTS `reversion_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reversion_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` longtext NOT NULL,
  `object_id_int` int(11) DEFAULT NULL,
  `format` varchar(255) NOT NULL,
  `serialized_data` longtext NOT NULL,
  `object_repr` longtext NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `revision_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `revers_content_type_id_c01a11926d4c4a9_fk_django_content_type_id` (`content_type_id`),
  KEY `reversion_v_revision_id_48ec3744916a950_fk_reversion_revision_id` (`revision_id`),
  KEY `reversion_version_0c9ba3a3` (`object_id_int`),
  CONSTRAINT `revers_content_type_id_c01a11926d4c4a9_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `reversion_v_revision_id_48ec3744916a950_fk_reversion_revision_id` FOREIGN KEY (`revision_id`) REFERENCES `reversion_revision` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_version`
--

LOCK TABLES `reversion_version` WRITE;
/*!40000 ALTER TABLE `reversion_version` DISABLE KEYS */;
INSERT INTO `reversion_version` VALUES (1,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 5368709120, \"used_file_size\": 0, \"contact\": \"8277121319\", \"address\": \"Sastry house, pragathi nagar, hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',9,1),(2,'2',2,'json','[{\"fields\": {\"website\": \"www.google.com\", \"name\": \"TestOrganization2\", \"total_file_size_limit\": 5368709120, \"used_file_size\": 0, \"contact\": \"9440806969\", \"address\": \"sanath nagar, hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 2}]','TestOrganization2',9,2),(3,'1',1,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-04-22\", \"description\": \"group created in bangalore by nipun\", \"created_by\": 8, \"group_name\": \"bangalore 1\"}, \"model\": \"screenManagement.group\", \"pk\": 1}]','bangalore 1',13,3),(4,'2',2,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-04-22\", \"description\": \"group created by nipun in bangalore 2\", \"created_by\": 8, \"group_name\": \"bangalore 2\"}, \"model\": \"screenManagement.group\", \"pk\": 2}]','bangalore 2',13,4),(5,'3',3,'json','[{\"fields\": {\"organization\": 2, \"created_on\": \"2016-04-22\", \"description\": \"Group created by kmpk123 in hyderabad\", \"created_by\": 9, \"group_name\": \"hyderabad 1\"}, \"model\": \"screenManagement.group\", \"pk\": 3}]','hyderabad 1',13,5),(6,'4',4,'json','[{\"fields\": {\"organization\": 2, \"created_on\": \"2016-04-22\", \"description\": \"Group created by kmpk123 in hyderabad 2\", \"created_by\": 9, \"group_name\": \"hyderabad 2\"}, \"model\": \"screenManagement.group\", \"pk\": 4}]','hyderabad 2',13,6),(7,'5',5,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-17\", \"description\": \"screens will be added in the future\", \"created_by\": 8, \"group_name\": \"empty group\"}, \"model\": \"screenManagement.group\", \"pk\": 5}]','empty group',13,7),(8,'6',6,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-17\", \"description\": \"temp group\", \"created_by\": 8, \"group_name\": \"temp group 2\"}, \"model\": \"screenManagement.group\", \"pk\": 6}]','temp group 2',13,8),(9,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": 1, \"created_by\": 8}, \"model\": \"screenManagement.groupscreens\", \"pk\": 1}]','bellandur 1-bangalore 1',37,9),(10,'2',2,'json','[{\"fields\": {\"screen\": 2, \"group\": 5, \"created_by\": 8}, \"model\": \"screenManagement.groupscreens\", \"pk\": 2}]','screen 2-empty group',37,10),(11,'1',1,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 3, \"activation_key\": \"\", \"activated_by\": 8, \"screen_name\": \"bellandur 1\", \"screen_calendar\": 1, \"screen_size\": 32, \"address\": \"bangalore central mall, bellandur\", \"aspect_ratio\": \"\", \"owned_by\": 1, \"activated_on\": \"2016-04-22\", \"resolution\": \"1024*768\", \"device_identification_id\": \"ASDF1234\"}, \"model\": \"screenManagement.screen\", \"pk\": 1}]','bellandur 1',15,11),(12,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 3, \"activation_key\": \"\", \"activated_by\": 8, \"screen_name\": \"screen 2\", \"screen_calendar\": 4, \"screen_size\": 50, \"address\": \"bangalore central mall, bellandur\", \"aspect_ratio\": \"\", \"owned_by\": 1, \"activated_on\": \"2016-04-22\", \"resolution\": \"1744*899\", \"device_identification_id\": \"ASDF6789\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','screen 2',15,12),(13,'3',3,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 2, \"activation_key\": \"qwertyui\", \"activated_by\": 9, \"screen_name\": \"hyd orbit 1\", \"screen_calendar\": null, \"screen_size\": 50, \"address\": \"11th floor, inorbit mall, hyderabad\", \"aspect_ratio\": \"16:9\", \"owned_by\": 2, \"activated_on\": \"2016-04-22\", \"resolution\": \"1024*768\", \"device_identification_id\": \"QWER1234\"}, \"model\": \"screenManagement.screen\", \"pk\": 3}]','hyd orbit 1',15,13),(14,'4',4,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 2, \"activation_key\": \"asdfghjk\", \"activated_by\": 9, \"screen_name\": \"hyd orbit 2\", \"screen_calendar\": null, \"screen_size\": 47, \"address\": \"12th floor, inorbit mall, hyderabad\", \"aspect_ratio\": \"16:9\", \"owned_by\": 2, \"activated_on\": \"2016-04-22\", \"resolution\": \"1024*768\", \"device_identification_id\": \"QWER0987\"}, \"model\": \"screenManagement.screen\", \"pk\": 4}]','hyd orbit 2',15,14),(15,'5',5,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 3, \"activation_key\": \"aassddff\", \"activated_by\": null, \"screen_name\": \"screen 3\", \"screen_calendar\": null, \"screen_size\": 33, \"address\": \"marathalli 7th main\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"activated_on\": null, \"resolution\": \"1024*768\", \"device_identification_id\": null}, \"model\": \"screenManagement.screen\", \"pk\": 5}]','screen 3',15,15),(16,'8',8,'json','[{\"fields\": {\"is_folder\": true, \"title\": \"Jaffa\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-04-24T14:38:49.933Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-04-24T14:38:49.934Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 8}]','Jaffa',17,16),(17,'21',21,'json','[{\"fields\": {\"is_folder\": true, \"title\": \"inside jaffa\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-04-25T06:00:56.622Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-04-25T06:00:56.622Z\", \"organization\": 1, \"parent_folder\": 8, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 21}]','inside jaffa',17,17),(18,'22',22,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"logo\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-04-25T06:01:21.569Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-04-25T06:01:21.569Z\", \"organization\": 1, \"parent_folder\": 8, \"document\": \"usercontent/8/blynq_logo.png\"}, \"model\": \"contentManagement.content\", \"pk\": 22}]','logo',17,18),(19,'23',23,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"groups ui\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-04-25T09:24:32.045Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-04-25T09:24:32.045Z\", \"organization\": 1, \"parent_folder\": 8, \"document\": \"usercontent/8/Groups UI.png\"}, \"model\": \"contentManagement.content\", \"pk\": 23}]','groups ui',17,19),(20,'24',24,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"logo\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-04-26T10:00:36.175Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-04-26T10:00:36.175Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"usercontent/8/blynq_logo_YZWVlEC.png\"}, \"model\": \"contentManagement.content\", \"pk\": 24}]','logo',17,20),(21,'25',25,'json','[{\"fields\": {\"is_folder\": true, \"title\": \"sastry\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-04T12:14:44.069Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-05-04T12:14:44.069Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 25}]','sastry',17,21),(22,'26',26,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"Flow diagram\", \"file_type\": null, \"last_modified_by\": 8, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-04T12:15:08.194Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 8, \"last_modified_time\": \"2016-05-04T12:15:08.194Z\", \"organization\": 1, \"parent_folder\": 25, \"document\": \"usercontent/8/flow_diagram.jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 26}]','Flow diagram',17,22),(23,'2',2,'json','[{\"fields\": {\"content\": 23, \"playlist\": 1, \"display_time\": 10, \"position_index\": 2}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 2}]','First playlist - groups ui',18,23),(24,'3',3,'json','[{\"fields\": {\"content\": 21, \"playlist\": 1, \"display_time\": 10, \"position_index\": 3}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 3}]','First playlist - inside jaffa',18,24),(25,'4',4,'json','[{\"fields\": {\"content\": 22, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 4}]','First playlist - logo',18,25),(26,'5',5,'json','[{\"fields\": {\"content\": 23, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 5}]','First playlist - groups ui',18,26),(27,'6',6,'json','[{\"fields\": {\"content\": 26, \"playlist\": 6, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 6}]','xyz - Flow diagram',18,27),(28,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-05-04T13:50:47.486Z\", \"created_by\": 8, \"last_updated_by\": 8, \"created_time\": \"2016-04-25T10:24:28.654Z\", \"organization\": 1, \"playlist_title\": \"First playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','First playlist',19,28),(29,'2',2,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-04-26T10:28:37.593Z\", \"created_by\": 8, \"last_updated_by\": 8, \"created_time\": \"2016-04-26T10:28:37.589Z\", \"organization\": 1, \"playlist_title\": \"abc\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 2}]','abc',19,29),(30,'4',4,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-04-26T10:30:16.399Z\", \"created_by\": 8, \"last_updated_by\": 8, \"created_time\": \"2016-04-26T10:30:16.398Z\", \"organization\": 1, \"playlist_title\": \"abc\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 4}]','abc',19,30),(31,'5',5,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-04-26T10:30:42.048Z\", \"created_by\": 8, \"last_updated_by\": 8, \"created_time\": \"2016-04-26T10:30:42.048Z\", \"organization\": 1, \"playlist_title\": \"playlist 2\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 5}]','playlist 2',19,31),(32,'6',6,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-05-04T12:18:29.089Z\", \"created_by\": 8, \"last_updated_by\": 8, \"created_time\": \"2016-05-04T12:17:48.785Z\", \"organization\": 1, \"playlist_title\": \"xyz\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 6}]','xyz',19,32),(33,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 2, \"schedule\": 1}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen bellandur 1',36,33),(34,'35',35,'json','[{\"fields\": {\"screen\": null, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - group empty group',36,34),(35,'1',1,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 1}]','First schedule-First playlist',35,35),(36,'2',2,'json','[{\"fields\": {\"playlist\": 5, \"position_index\": 1, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-playlist 2',35,36),(37,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','test schedule 1-First playlist',35,37),(38,'1',1,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 8, \"last_updated_time\": \"2016-05-17T09:52:40.305Z\", \"last_updated_by\": 8, \"is_always\": true, \"created_time\": \"2016-04-28T03:01:11.307Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 1}]','First schedule',21,38),(39,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 8, \"last_updated_time\": \"2016-05-17T19:26:03.606Z\", \"last_updated_by\": 8, \"is_always\": true, \"created_time\": \"2016-05-17T09:52:10.088Z\", \"organization\": 1, \"schedule_title\": \"test schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test schedule 1',21,39),(40,'36',36,'json','[{\"fields\": {\"screen\": 3, \"group\": 3, \"event\": 33, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 36}]','test schedule 1 - screen hyd orbit 1 - group hyderabad 1',36,40),(41,'36',36,'json','[{\"fields\": {\"screen\": 3, \"group\": 3, \"event\": 33, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 36}]','test schedule 1 - screen hyd orbit 1 - group hyderabad 1',36,41),(42,'35',35,'json','[{\"fields\": {\"screen\": 1, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - screen bellandur 1 - group empty group',36,42),(43,'35',35,'json','[{\"fields\": {\"screen\": null, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - group empty group',36,43),(44,'35',35,'json','[{\"fields\": {\"screen\": null, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - group empty group',36,44),(45,'35',35,'json','[{\"fields\": {\"screen\": 1, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - screen bellandur 1 - group empty group',36,45),(46,'35',35,'json','[{\"fields\": {\"screen\": null, \"group\": 5, \"event\": 35, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 35}]','test schedule 1 - group empty group',36,46),(47,'8',8,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-05-17T07:02:12.817Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$Mv4AbkbrBl55$iWTc/A7Thc64f3uU5TifJJmVyZyZajadB5r1QsnKrEc=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-04-22T11:12:38.176Z\"}, \"model\": \"auth.user\", \"pk\": 8}]','nipun',4,47),(48,'1',1,'json','[{\"fields\": {\"username\": \"admin\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-17T07:06:59.878Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$SqQofbBFt1mm$CsDDuv+oh4QcrJvMeadmQ+hiXsj6ofeBePlEgfEPU9s=\", \"email\": \"admin@gmail.com\", \"date_joined\": \"2016-04-22T06:32:39.913Z\"}, \"model\": \"auth.user\", \"pk\": 1}]','admin',4,48),(49,'9',9,'json','[{\"fields\": {\"username\": \"kmpk123\", \"first_name\": \"prasanth\", \"last_name\": \"kuriseti\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T11:15:34.224Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$R0ktrto3ZsYb$sS27znxrpJPEmSZZXacdS6fx6Ekp0wA9LpiCWpdmUDE=\", \"email\": \"kmpk123@gmail.com\", \"date_joined\": \"2016-04-22T11:13:09.428Z\"}, \"model\": \"auth.user\", \"pk\": 9}]','kmpk123',4,49),(50,'5',5,'json','[{\"fields\": {\"username\": \"jaydev\", \"first_name\": \"jaydev\", \"last_name\": \"kalivarapu\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T07:26:11.047Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$5MobmJBtYQzj$ZXSERJnNNZ2AQbqewdHrPecqC2A2PLVu/SK6/rYp3t0=\", \"email\": \"jaydev@gmail.com\", \"date_joined\": \"2016-04-22T07:25:49.122Z\"}, \"model\": \"auth.user\", \"pk\": 5}]','jaydev',4,50),(51,'7',7,'json','[{\"fields\": {\"username\": \"blynq\", \"first_name\": \"blynq\", \"last_name\": \"technologies\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T11:11:54.410Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$PUxTJLrDbayP$AHpHYc6EmoZrPrCoWKYEan9LxHF/lyzr+wtk2xUZC5M=\", \"email\": \"blynq@gmail.com\", \"date_joined\": \"2016-04-22T11:11:38.974Z\"}, \"model\": \"auth.user\", \"pk\": 7}]','blynq',4,51),(52,'8',8,'json','[{\"fields\": {\"organization\": 1, \"role\": 2, \"mobile_number\": \"+91827712131\"}, \"model\": \"authentication.userdetails\", \"pk\": 8}]','nipun',11,52),(53,'8',8,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-05-17T07:02:12.817Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$Mv4AbkbrBl55$iWTc/A7Thc64f3uU5TifJJmVyZyZajadB5r1QsnKrEc=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-04-22T11:12:38.176Z\"}, \"model\": \"auth.user\", \"pk\": 8}]','nipun',4,52),(54,'9',9,'json','[{\"fields\": {\"organization\": 2, \"role\": 3, \"mobile_number\": \"1234567890\"}, \"model\": \"authentication.userdetails\", \"pk\": 9}]','kmpk123',11,53),(55,'9',9,'json','[{\"fields\": {\"username\": \"kmpk123\", \"first_name\": \"prasanth\", \"last_name\": \"kuriseti\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T11:15:34.224Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$R0ktrto3ZsYb$sS27znxrpJPEmSZZXacdS6fx6Ekp0wA9LpiCWpdmUDE=\", \"email\": \"kmpk123@gmail.com\", \"date_joined\": \"2016-04-22T11:13:09.428Z\"}, \"model\": \"auth.user\", \"pk\": 9}]','kmpk123',4,53),(56,'5',5,'json','[{\"fields\": {\"organization\": 1, \"role\": 2, \"mobile_number\": \"1234567890\"}, \"model\": \"authentication.userdetails\", \"pk\": 5}]','jaydev',11,54),(57,'5',5,'json','[{\"fields\": {\"username\": \"jaydev\", \"first_name\": \"jaydev\", \"last_name\": \"kalivarapu\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T07:26:11.047Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$5MobmJBtYQzj$ZXSERJnNNZ2AQbqewdHrPecqC2A2PLVu/SK6/rYp3t0=\", \"email\": \"jaydev@gmail.com\", \"date_joined\": \"2016-04-22T07:25:49.122Z\"}, \"model\": \"auth.user\", \"pk\": 5}]','jaydev',4,54),(58,'7',7,'json','[{\"fields\": {\"username\": \"blynq\", \"first_name\": \"blynq\", \"last_name\": \"technologies\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-04-22T11:11:54.410Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$PUxTJLrDbayP$AHpHYc6EmoZrPrCoWKYEan9LxHF/lyzr+wtk2xUZC5M=\", \"email\": \"blynq@gmail.com\", \"date_joined\": \"2016-04-22T11:11:38.974Z\"}, \"model\": \"auth.user\", \"pk\": 7}]','blynq',4,55),(59,'7',7,'json','[{\"fields\": {\"organization\": 1, \"role\": 3, \"mobile_number\": \"8277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 7}]','blynq',11,55),(60,'8',8,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-05-24T05:45:03.232Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$Mv4AbkbrBl55$iWTc/A7Thc64f3uU5TifJJmVyZyZajadB5r1QsnKrEc=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-04-22T11:12:38.176Z\"}, \"model\": \"auth.user\", \"pk\": 8}]','nipun',4,56),(61,'8',8,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": \"2016-05-24T05:45:25.507Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$Mv4AbkbrBl55$iWTc/A7Thc64f3uU5TifJJmVyZyZajadB5r1QsnKrEc=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-04-22T11:12:38.176Z\"}, \"model\": \"auth.user\", \"pk\": 8}]','nipun',4,57),(62,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T09:36:43.094Z\", \"last_updated_by\": 8, \"is_always\": true, \"created_time\": \"2016-05-17T09:52:10.088Z\", \"organization\": 1, \"schedule_title\": \"test schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test schedule 1',21,58),(63,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','test schedule 1-First playlist',35,58),(64,'37',37,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 36, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 37}]','test schedule 1 - screen bellandur 1',36,58),(65,'1',1,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T09:38:06.543Z\", \"last_updated_by\": 8, \"is_always\": true, \"created_time\": \"2016-04-28T03:01:11.307Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 1}]','First schedule',21,59),(66,'2',2,'json','[{\"fields\": {\"playlist\": 5, \"position_index\": 1, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-playlist 2',35,59),(67,'1',1,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 1}]','First schedule-First playlist',35,59),(68,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 2, \"schedule\": 1}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen bellandur 1',36,59),(69,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T09:38:10.395Z\", \"last_updated_by\": 8, \"is_always\": true, \"created_time\": \"2016-05-17T09:52:10.088Z\", \"organization\": 1, \"schedule_title\": \"test schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test schedule 1',21,60),(70,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','test schedule 1-First playlist',35,60),(71,'37',37,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 36, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 37}]','test schedule 1 - screen bellandur 1',36,60),(72,'1',1,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": false, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T10:44:19.385Z\", \"last_updated_by\": 8, \"is_always\": false, \"created_time\": \"2016-04-28T03:01:11.307Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 1}]','First schedule',21,61),(73,'2',2,'json','[{\"fields\": {\"playlist\": 5, \"position_index\": 1, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-playlist 2',35,61),(74,'1',1,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 1}]','First schedule-First playlist',35,61),(75,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 2, \"schedule\": 1}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen bellandur 1',36,61),(76,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": false, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T10:44:47.632Z\", \"last_updated_by\": 8, \"is_always\": false, \"created_time\": \"2016-05-17T09:52:10.088Z\", \"organization\": 1, \"schedule_title\": \"test schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test schedule 1',21,62),(77,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','test schedule 1-First playlist',35,62),(78,'37',37,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 36, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 37}]','test schedule 1 - screen bellandur 1',36,62),(79,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": false, \"created_by\": 8, \"last_updated_time\": \"2016-05-24T10:45:00.923Z\", \"last_updated_by\": 8, \"is_always\": false, \"created_time\": \"2016-05-17T09:52:10.088Z\", \"organization\": 1, \"schedule_title\": \"test schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test schedule 1',21,63),(80,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','test schedule 1-First playlist',35,63),(81,'37',37,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 36, \"schedule\": 19}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 37}]','test schedule 1 - screen bellandur 1',36,63);
/*!40000 ALTER TABLE `reversion_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_schedule`
--

DROP TABLE IF EXISTS `scheduleManagement_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_schedule` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_title` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `last_updated_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `is_always` tinyint(1) NOT NULL,
  `recurrence_absolute` tinyint(1) NOT NULL,
  `all_day` tinyint(1) NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `b405690da41b1b8e66ba521e8f2675f6` (`created_by_id`),
  KEY `D0008ec854458223fc0440e7f59934e8` (`last_updated_by_id`),
  KEY `scheduleManagement_schedule_26b2345e` (`organization_id`),
  CONSTRAINT `D0008ec854458223fc0440e7f59934e8` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `D1e8960ced6145002a4e9f87736e58c2` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `b405690da41b1b8e66ba521e8f2675f6` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedule`
--

LOCK TABLES `scheduleManagement_schedule` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedule` DISABLE KEYS */;
INSERT INTO `scheduleManagement_schedule` VALUES (1,'First schedule','2016-04-28 03:01:11.307795','2016-05-24 10:44:19.385791',8,8,1,0,0,0),(19,'test schedule 1','2016-05-17 09:52:10.088950','2016-05-24 10:45:00.923710',8,8,1,0,0,0);
/*!40000 ALTER TABLE `scheduleManagement_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_scheduleplaylists`
--

DROP TABLE IF EXISTS `scheduleManagement_scheduleplaylists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_scheduleplaylists` (
  `schedule_playlist_id` int(11) NOT NULL AUTO_INCREMENT,
  `position_index` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `schedule_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`schedule_playlist_id`),
  KEY `D14cbb3d9d04709e1c3e85ecef80ff83` (`playlist_id`),
  KEY `scheduleManagement_scheduleplaylists_9bc70bb9` (`schedule_id`),
  CONSTRAINT `D14cbb3d9d04709e1c3e85ecef80ff83` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`playlist_id`),
  CONSTRAINT `fae4cee4482027edf411bf20126c431d` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_scheduleplaylists`
--

LOCK TABLES `scheduleManagement_scheduleplaylists` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_scheduleplaylists` DISABLE KEYS */;
INSERT INTO `scheduleManagement_scheduleplaylists` VALUES (1,0,1,1),(2,1,5,1),(21,0,1,19);
/*!40000 ALTER TABLE `scheduleManagement_scheduleplaylists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_schedulescreens`
--

DROP TABLE IF EXISTS `scheduleManagement_schedulescreens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_schedulescreens` (
  `schedule_screen_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `schedule_id` int(11) NOT NULL,
  `screen_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`schedule_screen_id`),
  UNIQUE KEY `scheduleManagement_schedulescreen_event_id_151cbcd7ab0f3afc_uniq` (`event_id`),
  KEY `scheduleManagemen_event_id_151cbcd7ab0f3afc_fk_schedule_event_id` (`event_id`),
  KEY `sch_group_id_1f92042eee00a477_fk_screenManagement_group_group_id` (`group_id`),
  KEY `scheduleManagement_schedulescreens_9bc70bb9` (`schedule_id`),
  KEY `scheduleManagement_schedulescreens_e4ec8585` (`screen_id`),
  CONSTRAINT `D29edf893c4f7c5fbba5410fe2ce1ccd` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`),
  CONSTRAINT `sch_group_id_1f92042eee00a477_fk_screenManagement_group_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`group_id`),
  CONSTRAINT `scheduleManagemen_event_id_151cbcd7ab0f3afc_fk_schedule_event_id` FOREIGN KEY (`event_id`) REFERENCES `schedule_event` (`id`),
  CONSTRAINT `screen_id_5aa6103c3cd0e0ad_fk_screenManagement_screen_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`screen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedulescreens`
--

LOCK TABLES `scheduleManagement_schedulescreens` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedulescreens` DISABLE KEYS */;
INSERT INTO `scheduleManagement_schedulescreens` VALUES (1,2,NULL,1,1),(37,36,NULL,19,1);
/*!40000 ALTER TABLE `scheduleManagement_schedulescreens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_calendar`
--

DROP TABLE IF EXISTS `schedule_calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `slug` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_calendar_2dbcba41` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_calendar`
--

LOCK TABLES `schedule_calendar` WRITE;
/*!40000 ALTER TABLE `schedule_calendar` DISABLE KEYS */;
INSERT INTO `schedule_calendar` VALUES (1,'Flipkart Calendar','flipkart-calendar'),(2,'amazon calendar','amazon-calendar'),(3,'default','default'),(4,'screen 2','');
/*!40000 ALTER TABLE `schedule_calendar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_calendarrelation`
--

DROP TABLE IF EXISTS `schedule_calendarrelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_calendarrelation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `distinction` varchar(20) DEFAULT NULL,
  `inheritable` tinyint(1) NOT NULL,
  `calendar_id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_ca_calendar_id_514da443becc84e7_fk_schedule_calendar_id` (`calendar_id`),
  KEY `sched_content_type_id_47ce4c2ee10c0563_fk_django_content_type_id` (`content_type_id`),
  CONSTRAINT `sched_content_type_id_47ce4c2ee10c0563_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `schedule_ca_calendar_id_514da443becc84e7_fk_schedule_calendar_id` FOREIGN KEY (`calendar_id`) REFERENCES `schedule_calendar` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_calendarrelation`
--

LOCK TABLES `schedule_calendarrelation` WRITE;
/*!40000 ALTER TABLE `schedule_calendarrelation` DISABLE KEYS */;
INSERT INTO `schedule_calendarrelation` VALUES (1,1,'f1',1,1,21);
/*!40000 ALTER TABLE `schedule_calendarrelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_event`
--

DROP TABLE IF EXISTS `schedule_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start` datetime(6) NOT NULL,
  `end` datetime(6) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `end_recurring_period` datetime(6) DEFAULT NULL,
  `calendar_id` int(11) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `rule_id` int(11) DEFAULT NULL,
  `color_event` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_ev_calendar_id_4c9dba94868bbeb0_fk_schedule_calendar_id` (`calendar_id`),
  KEY `schedule_event_creator_id_f3a6304c337da5b_fk_auth_user_id` (`creator_id`),
  KEY `schedule_event_e1150e65` (`rule_id`),
  CONSTRAINT `schedule_ev_calendar_id_4c9dba94868bbeb0_fk_schedule_calendar_id` FOREIGN KEY (`calendar_id`) REFERENCES `schedule_calendar` (`id`),
  CONSTRAINT `schedule_event_creator_id_f3a6304c337da5b_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `schedule_event_rule_id_41a281cbfafd8f64_fk_schedule_rule_id` FOREIGN KEY (`rule_id`) REFERENCES `schedule_rule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_event`
--

LOCK TABLES `schedule_event` WRITE;
/*!40000 ALTER TABLE `schedule_event` DISABLE KEYS */;
INSERT INTO `schedule_event` VALUES (2,'2016-05-24 02:30:00.000000','2016-05-24 12:00:00.000000','First schedule','Nothing much','2016-04-28 02:30:52.376234','2016-05-24 10:44:19.462124','2016-05-24 12:00:00.000000',1,8,22,NULL),(4,'2016-05-14 00:00:00.000000','2016-05-14 23:59:59.000000','Full day event','','2016-05-14 07:44:50.515432','2016-05-14 07:44:50.515479','2016-05-18 07:44:46.000000',1,8,NULL,NULL),(35,'2016-05-17 00:00:00.622782','2016-05-17 23:59:59.622823','test schedule 1',NULL,'2016-05-17 10:07:44.355605','2016-05-17 10:07:44.355634',NULL,3,8,18,NULL),(36,'2016-05-24 02:30:00.000000','2016-05-24 15:00:00.000000','test schedule 1',NULL,'2016-05-24 09:36:43.131073','2016-05-24 10:45:00.944786','2016-05-24 15:00:00.000000',1,8,24,NULL);
/*!40000 ALTER TABLE `schedule_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_eventrelation`
--

DROP TABLE IF EXISTS `schedule_eventrelation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_eventrelation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_id` int(11) NOT NULL,
  `distinction` varchar(20) DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sched_content_type_id_59125ed578fc01c4_fk_django_content_type_id` (`content_type_id`),
  KEY `schedule_eventrel_event_id_59ac87f9ff34638b_fk_schedule_event_id` (`event_id`),
  CONSTRAINT `sched_content_type_id_59125ed578fc01c4_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `schedule_eventrel_event_id_59ac87f9ff34638b_fk_schedule_event_id` FOREIGN KEY (`event_id`) REFERENCES `schedule_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_eventrelation`
--

LOCK TABLES `schedule_eventrelation` WRITE;
/*!40000 ALTER TABLE `schedule_eventrelation` DISABLE KEYS */;
/*!40000 ALTER TABLE `schedule_eventrelation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_occurrence`
--

DROP TABLE IF EXISTS `schedule_occurrence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_occurrence` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` longtext,
  `start` datetime(6) NOT NULL,
  `end` datetime(6) NOT NULL,
  `cancelled` tinyint(1) NOT NULL,
  `original_start` datetime(6) NOT NULL,
  `original_end` datetime(6) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `updated_on` datetime(6) NOT NULL,
  `event_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `schedule_occurren_event_id_2bf84479e33c039d_fk_schedule_event_id` (`event_id`),
  CONSTRAINT `schedule_occurren_event_id_2bf84479e33c039d_fk_schedule_event_id` FOREIGN KEY (`event_id`) REFERENCES `schedule_event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_occurrence`
--

LOCK TABLES `schedule_occurrence` WRITE;
/*!40000 ALTER TABLE `schedule_occurrence` DISABLE KEYS */;
/*!40000 ALTER TABLE `schedule_occurrence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_rule`
--

DROP TABLE IF EXISTS `schedule_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schedule_rule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` longtext NOT NULL,
  `frequency` varchar(10) NOT NULL,
  `params` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_rule`
--

LOCK TABLES `schedule_rule` WRITE;
/*!40000 ALTER TABLE `schedule_rule` DISABLE KEYS */;
INSERT INTO `schedule_rule` VALUES (1,'Month start sale','This sale starts every month on 1st','MONTHLY',''),(3,'Every monday, tuesday fortnight','Select monday and tuesday once in every two weeks','DAILY','interval:3'),(5,'default-weekly','This is a basic rule recurring weekly. No params should be set for this','WEEKLY',''),(6,'default-yearly','This is a basic rule recurring yearly. No params should be set for this','YEARLY',''),(8,'default-monthly','This is a basic rule recurring monthly. No params should be set for this','MONTHLY',''),(9,'test','test','WEEKLY',NULL),(11,'test schedule 1','test schedule 1','DAILY',NULL),(12,'test schedule 1','test schedule 1','DAILY',NULL),(13,'test schedule 1','test schedule 1','DAILY',NULL),(14,'test schedule 1','test schedule 1','DAILY',NULL),(15,'test schedule 1','test schedule 1','DAILY',NULL),(16,'test schedule 1','test schedule 1','DAILY',NULL),(17,'test schedule 1','test schedule 1','DAILY',NULL),(18,'test schedule 1','test schedule 1','DAILY',NULL),(22,'First schedule','First schedule','DAILY','interval:1;;;;'),(24,'test schedule 1','test schedule 1','DAILY','interval:1;;;;');
/*!40000 ALTER TABLE `schedule_rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_group`
--

DROP TABLE IF EXISTS `screenManagement_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_group` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL,
  `description` longtext,
  `created_on` date NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `organization_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`group_id`),
  KEY `f4d416adc879a6e27bc401a773527249` (`created_by_id`),
  KEY `screenManagement_group_26b2345e` (`organization_id`),
  CONSTRAINT `a336d8d83dbde3af1e27c50bab159d86` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `f4d416adc879a6e27bc401a773527249` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_group`
--

LOCK TABLES `screenManagement_group` WRITE;
/*!40000 ALTER TABLE `screenManagement_group` DISABLE KEYS */;
INSERT INTO `screenManagement_group` VALUES (1,'bangalore 1','group created in bangalore by nipun','2016-04-22',8,1),(2,'bangalore 2','group created by nipun in bangalore 2','2016-04-22',8,1),(3,'hyderabad 1','Group created by kmpk123 in hyderabad','2016-04-22',9,2),(4,'hyderabad 2','Group created by kmpk123 in hyderabad 2','2016-04-22',9,2),(5,'empty group','screens will be added in the future','2016-05-17',8,1),(6,'temp group 2','temp group','2016-05-17',8,1);
/*!40000 ALTER TABLE `screenManagement_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_groupscreens`
--

DROP TABLE IF EXISTS `screenManagement_groupscreens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_groupscreens` (
  `group_screen_id` int(11) NOT NULL AUTO_INCREMENT,
  `created_by_id` int(11) DEFAULT NULL,
  `group_id` int(11) NOT NULL,
  `screen_id` int(11) NOT NULL,
  PRIMARY KEY (`group_screen_id`),
  KEY `d895d1a320b1ec8690741d98f978e9cf` (`created_by_id`),
  KEY `scr_group_id_25d38b0ae3064275_fk_screenManagement_group_group_id` (`group_id`),
  KEY `screenManagement_groupscreens_e4ec8585` (`screen_id`),
  CONSTRAINT `d895d1a320b1ec8690741d98f978e9cf` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `s_screen_id_168b1902c060aef_fk_screenManagement_screen_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`screen_id`),
  CONSTRAINT `scr_group_id_25d38b0ae3064275_fk_screenManagement_group_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_groupscreens`
--

LOCK TABLES `screenManagement_groupscreens` WRITE;
/*!40000 ALTER TABLE `screenManagement_groupscreens` DISABLE KEYS */;
INSERT INTO `screenManagement_groupscreens` VALUES (1,8,1,1);
/*!40000 ALTER TABLE `screenManagement_groupscreens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screen`
--

DROP TABLE IF EXISTS `screenManagement_screen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screen` (
  `screen_id` int(11) NOT NULL AUTO_INCREMENT,
  `screen_name` varchar(100) NOT NULL,
  `screen_size` int(11) DEFAULT NULL,
  `aspect_ratio` varchar(20) DEFAULT NULL,
  `resolution` varchar(20) DEFAULT NULL,
  `address` varchar(100) NOT NULL,
  `activated_on` datetime(6) NOT NULL,
  `business_type` varchar(20) NOT NULL,
  `activated_by_id` int(11) DEFAULT NULL,
  `owned_by_id` int(11) DEFAULT NULL,
  `status_id` int(11) NOT NULL,
  `screen_calendar_id` int(11) DEFAULT NULL,
  `unique_device_key_id` int(11) NOT NULL,
  PRIMARY KEY (`screen_id`),
  UNIQUE KEY `activation_key_id` (`unique_device_key_id`),
  KEY `ebc63bdd0f179da0d15ee30f124ea0e0` (`activated_by_id`),
  KEY `a7c1ba1e3d46eee1df95a619a8c2f227` (`owned_by_id`),
  KEY `screenManagement_screen_dc91ed4b` (`status_id`),
  KEY `screenManagement_screen_b1831bbb` (`screen_calendar_id`),
  CONSTRAINT `D099a9619f8d384185c59ce135083230` FOREIGN KEY (`unique_device_key_id`) REFERENCES `screenManagement_screenactivationkey` (`screen_activation_id`),
  CONSTRAINT `D23b29036e98defa308670106fdeab4f` FOREIGN KEY (`status_id`) REFERENCES `screenManagement_screenstatus` (`screen_status_id`),
  CONSTRAINT `a7c1ba1e3d46eee1df95a619a8c2f227` FOREIGN KEY (`owned_by_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `ebc63bdd0f179da0d15ee30f124ea0e0` FOREIGN KEY (`activated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `scre_screen_calendar_id_58aceaff89f25de5_fk_schedule_calendar_id` FOREIGN KEY (`screen_calendar_id`) REFERENCES `schedule_calendar` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screen`
--

LOCK TABLES `screenManagement_screen` WRITE;
/*!40000 ALTER TABLE `screenManagement_screen` DISABLE KEYS */;
INSERT INTO `screenManagement_screen` VALUES (1,'bellandur 1',32,'','1024*768','bangalore central mall, bellandur','2016-04-22 00:00:00.000000','PRIVATE',8,1,3,1,1);
/*!40000 ALTER TABLE `screenManagement_screen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screenactivationkey`
--

DROP TABLE IF EXISTS `screenManagement_screenactivationkey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screenactivationkey` (
  `screen_activation_id` int(11) NOT NULL AUTO_INCREMENT,
  `activation_key` varchar(16) NOT NULL,
  `device_serial_num` varchar(20) NOT NULL,
  `in_use` tinyint(1) NOT NULL,
  PRIMARY KEY (`screen_activation_id`),
  UNIQUE KEY `activation_key` (`activation_key`),
  UNIQUE KEY `device_serial_num` (`device_serial_num`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenactivationkey`
--

LOCK TABLES `screenManagement_screenactivationkey` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenactivationkey` DISABLE KEYS */;
INSERT INTO `screenManagement_screenactivationkey` VALUES (1,'0123456789','RDPPC 117136',0);
/*!40000 ALTER TABLE `screenManagement_screenactivationkey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screenspecs`
--

DROP TABLE IF EXISTS `screenManagement_screenspecs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screenspecs` (
  `screen_specs_id` int(11) NOT NULL AUTO_INCREMENT,
  `brand` varchar(50) NOT NULL,
  `model_num` varchar(50) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `dimensions` varchar(50) DEFAULT NULL,
  `display_type` varchar(10) DEFAULT NULL,
  `contrast_ratio` varchar(20) DEFAULT NULL,
  `wattage` int(11) DEFAULT NULL,
  `additional_details` longtext,
  PRIMARY KEY (`screen_specs_id`),
  UNIQUE KEY `screenManagement_screenspecs_brand_3dc574781c54ace9_uniq` (`brand`,`model_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenspecs`
--

LOCK TABLES `screenManagement_screenspecs` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenspecs` DISABLE KEYS */;
/*!40000 ALTER TABLE `screenManagement_screenspecs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screenstatus`
--

DROP TABLE IF EXISTS `screenManagement_screenstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screenstatus` (
  `screen_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`screen_status_id`),
  UNIQUE KEY `status_name` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenstatus`
--

LOCK TABLES `screenManagement_screenstatus` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenstatus` DISABLE KEYS */;
INSERT INTO `screenManagement_screenstatus` VALUES (1,'Unactivated','The screen is not activated yet.'),(2,'Online','The screen is on and is currently scheduling content.'),(3,'Offline','The screen is either off or doesn\'t have the internet connectivity.'),(4,'Idle','The screen is on and has internet connectivity but there is no content scheduled.');
/*!40000 ALTER TABLE `screenManagement_screenstatus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-24 19:22:05
