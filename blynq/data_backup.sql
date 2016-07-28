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
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add calendar',7,'add_calendar'),(20,'Can change calendar',7,'change_calendar'),(21,'Can delete calendar',7,'delete_calendar'),(22,'Can add calendar relation',8,'add_calendarrelation'),(23,'Can change calendar relation',8,'change_calendarrelation'),(24,'Can delete calendar relation',8,'delete_calendarrelation'),(25,'Can add rule',9,'add_rule'),(26,'Can change rule',9,'change_rule'),(27,'Can delete rule',9,'delete_rule'),(28,'Can add event',10,'add_event'),(29,'Can change event',10,'change_event'),(30,'Can delete event',10,'delete_event'),(31,'Can add event relation',11,'add_eventrelation'),(32,'Can change event relation',11,'change_eventrelation'),(33,'Can delete event relation',11,'delete_eventrelation'),(34,'Can add occurrence',12,'add_occurrence'),(35,'Can change occurrence',12,'change_occurrence'),(36,'Can delete occurrence',12,'delete_occurrence'),(37,'Can add revision',13,'add_revision'),(38,'Can change revision',13,'change_revision'),(39,'Can delete revision',13,'delete_revision'),(40,'Can add version',14,'add_version'),(41,'Can change version',14,'change_version'),(42,'Can delete version',14,'delete_version'),(43,'Can add city',15,'add_city'),(44,'Can change city',15,'change_city'),(45,'Can delete city',15,'delete_city'),(49,'Can add organization',17,'add_organization'),(50,'Can change organization',17,'change_organization'),(51,'Can delete organization',17,'delete_organization'),(52,'Can add role',18,'add_role'),(53,'Can change role',18,'change_role'),(54,'Can delete role',18,'delete_role'),(55,'Can add user details',19,'add_userdetails'),(56,'Can change user details',19,'change_userdetails'),(57,'Can delete user details',19,'delete_userdetails'),(58,'Can add requested quote',20,'add_requestedquote'),(59,'Can change requested quote',20,'change_requestedquote'),(60,'Can delete requested quote',20,'delete_requestedquote'),(61,'Can add screen status',21,'add_screenstatus'),(62,'Can change screen status',21,'change_screenstatus'),(63,'Can delete screen status',21,'delete_screenstatus'),(67,'Can add screen activation key',23,'add_screenactivationkey'),(68,'Can change screen activation key',23,'change_screenactivationkey'),(69,'Can delete screen activation key',23,'delete_screenactivationkey'),(70,'Can add group',24,'add_group'),(71,'Can change group',24,'change_group'),(72,'Can delete group',24,'delete_group'),(73,'Can add group screens',25,'add_groupscreens'),(74,'Can change group screens',25,'change_groupscreens'),(75,'Can delete group screens',25,'delete_groupscreens'),(76,'Can add screen',26,'add_screen'),(77,'Can change screen',26,'change_screen'),(78,'Can delete screen',26,'delete_screen'),(82,'Can add content',28,'add_content'),(83,'Can change content',28,'change_content'),(84,'Can delete content',28,'delete_content'),(85,'Can add playlist items',29,'add_playlistitems'),(86,'Can change playlist items',29,'change_playlistitems'),(87,'Can delete playlist items',29,'delete_playlistitems'),(88,'Can add playlist',30,'add_playlist'),(89,'Can change playlist',30,'change_playlist'),(90,'Can delete playlist',30,'delete_playlist'),(94,'Can add schedule playlists',32,'add_scheduleplaylists'),(95,'Can change schedule playlists',32,'change_scheduleplaylists'),(96,'Can delete schedule playlists',32,'delete_scheduleplaylists'),(97,'Can add schedule',33,'add_schedule'),(98,'Can change schedule',33,'change_schedule'),(99,'Can delete schedule',33,'delete_schedule'),(103,'Can add content type',35,'add_contenttype'),(104,'Can change content type',35,'change_contenttype'),(105,'Can delete content type',35,'delete_contenttype'),(112,'Can add player update',38,'add_playerupdate'),(113,'Can change player update',38,'change_playerupdate'),(114,'Can delete player update',38,'delete_playerupdate'),(115,'Can add local server',39,'add_localserver'),(116,'Can change local server',39,'change_localserver'),(117,'Can delete local server',39,'delete_localserver'),(136,'Can add schedule pane',46,'add_schedulepane'),(137,'Can change schedule pane',46,'change_schedulepane'),(138,'Can delete schedule pane',46,'delete_schedulepane'),(139,'Can add schedule screens',47,'add_schedulescreens'),(140,'Can change schedule screens',47,'change_schedulescreens'),(141,'Can delete schedule screens',47,'delete_schedulescreens'),(142,'Can add aspect ratio',48,'add_aspectratio'),(143,'Can change aspect ratio',48,'change_aspectratio'),(144,'Can delete aspect ratio',48,'delete_aspectratio'),(145,'Can add layout pane',49,'add_layoutpane'),(146,'Can change layout pane',49,'change_layoutpane'),(147,'Can delete layout pane',49,'delete_layoutpane'),(148,'Can add layout',50,'add_layout'),(149,'Can change layout',50,'change_layout'),(150,'Can delete layout',50,'delete_layout');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=','2016-05-28 13:20:05.178153',1,'admin','','','hello@blynq.in',1,1,'2016-05-27 10:29:30.217333'),(2,'pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=','2016-07-28 03:22:40.885275',1,'nipun','Nipun','Edara','nipun425@gmail.com',1,1,'2016-05-27 10:32:28.000000');
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
-- Table structure for table `authentication_city`
--

DROP TABLE IF EXISTS `authentication_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `name` (`city_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_city`
--

LOCK TABLES `authentication_city` WRITE;
/*!40000 ALTER TABLE `authentication_city` DISABLE KEYS */;
INSERT INTO `authentication_city` VALUES (1,'Hyderabad','Telangana'),(2,'Visakhapatnam','Andhra Pradesh'),(3,'kakinada','Andhra Pradesh');
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
  `organization_name` varchar(100) NOT NULL,
  `website` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `total_file_size_limit` bigint(20) NOT NULL,
  `used_file_size` bigint(20) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE KEY `name` (`organization_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_organization`
--

LOCK TABLES `authentication_organization` WRITE;
/*!40000 ALTER TABLE `authentication_organization` DISABLE KEYS */;
INSERT INTO `authentication_organization` VALUES (1,'Blynq Pvt Ltd','http://www.blynq.in','G1, Mount Fort, Pragathi Nagar, Hyderabad','8277121319',1073741824,22762080);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_requestedquote`
--

LOCK TABLES `authentication_requestedquote` WRITE;
/*!40000 ALTER TABLE `authentication_requestedquote` DISABLE KEYS */;
INSERT INTO `authentication_requestedquote` VALUES (1,'nipun','nipun425@gmail.com','8277121319',5,'asdfasdf','2016-06-01 08:17:33.622344');
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
  `description` varchar(100),
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_role`
--

LOCK TABLES `authentication_role` WRITE;
/*!40000 ALTER TABLE `authentication_role` DISABLE KEYS */;
INSERT INTO `authentication_role` VALUES (1,'manager',NULL);
/*!40000 ALTER TABLE `authentication_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_userdetails`
--

DROP TABLE IF EXISTS `authentication_userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_userdetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mobile_number` varchar(12) NOT NULL,
  `organization_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `f6a950242aa695a19cf9a8637c2378a7` (`organization_id`),
  KEY `authenti_role_id_44612207d2201d34_fk_authentication_role_role_id` (`role_id`),
  CONSTRAINT `authenti_role_id_44612207d2201d34_fk_authentication_role_role_id` FOREIGN KEY (`role_id`) REFERENCES `authentication_role` (`role_id`),
  CONSTRAINT `authentication_userdeta_user_id_5d1f3335ca1df751_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `f6a950242aa695a19cf9a8637c2378a7` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_userdetails`
--

LOCK TABLES `authentication_userdetails` WRITE;
/*!40000 ALTER TABLE `authentication_userdetails` DISABLE KEYS */;
INSERT INTO `authentication_userdetails` VALUES (1,'918277121319',1,1,2);
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
  `uploaded_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `is_folder` tinyint(1) NOT NULL,
  `relative_path` varchar(1025) NOT NULL,
  `last_modified_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `parent_folder_id` int(11) DEFAULT NULL,
  `uploaded_by_id` int(11) DEFAULT NULL,
  `url` varchar(255),
  `content_type_id` int(11),
  PRIMARY KEY (`content_id`),
  KEY `D5bd4182a66a7dc9e4dbc49d79b84d24` (`last_modified_by_id`),
  KEY `D030273c9e61c272ad95472f688031ac` (`organization_id`),
  KEY `c28200b62fd5064ce5f884826faee3c7` (`parent_folder_id`),
  KEY `D9406e8f168fd432bee791784e0f2ca1` (`uploaded_by_id`),
  KEY `contentManagement_content_417f1b1c` (`content_type_id`),
  CONSTRAINT `D030273c9e61c272ad95472f688031ac` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `D5bd4182a66a7dc9e4dbc49d79b84d24` FOREIGN KEY (`last_modified_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `D9406e8f168fd432bee791784e0f2ca1` FOREIGN KEY (`uploaded_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `b742e9ac5b1be573dde092d3e2531d1b` FOREIGN KEY (`content_type_id`) REFERENCES `contentManagement_contenttype` (`content_type_id`),
  CONSTRAINT `c28200b62fd5064ce5f884826faee3c7` FOREIGN KEY (`parent_folder_id`) REFERENCES `contentManagement_content` (`content_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_content`
--

LOCK TABLES `contentManagement_content` WRITE;
/*!40000 ALTER TABLE `contentManagement_content` DISABLE KEYS */;
INSERT INTO `contentManagement_content` VALUES (11,'sachin','usercontent/1/sachin.jpg','','2016-05-31 19:39:58.628638','2016-06-11 07:28:19.322548',0,'/',1,1,NULL,1,'/media/usercontent/1/sachin.jpg',8),(14,'SREEJAKALYANAM II CHIRANJEEVI DAUGHTER  Wedding Trailer II EPICS BY AVINASH-QL0BsNLG1qY','test_usercontent/user1/SREEJAKALYANAM II CHIRANJEEVI DAUGHTER  Wedding Trailer II EPICS _PGqKlDA.mp4','','2016-06-28 08:15:53.137376','2016-06-28 08:15:53.137514',0,'/',1,1,NULL,1,NULL,6),(38,'charlie chaplin','test_usercontent/user1/converted_charlie chaplin.mp4','','2016-07-05 08:34:08.784963','2016-07-05 08:34:08.785131',0,'/',1,1,NULL,1,NULL,6);
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
  `file_type` varchar(30) NOT NULL,
  `supported_encodings` longtext,
  PRIMARY KEY (`content_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_contenttype`
--

LOCK TABLES `contentManagement_contenttype` WRITE;
/*!40000 ALTER TABLE `contentManagement_contenttype` DISABLE KEYS */;
INSERT INTO `contentManagement_contenttype` VALUES (2,'url/web/iframe',''),(3,'url/web/youtube',''),(4,'file/image/gif',''),(5,'file/application/pdf',''),(6,'file/video/mp4','H.263,H.264'),(7,'file/video/3gpp',''),(8,'file/image/jpeg',''),(9,'file/image/png',''),(10,'file/image/bmp',''),(11,'file/image/webp',''),(12,'url/image/webp',''),(13,'url/image/jpeg',''),(14,'url/image/bmp',''),(15,'url/image/png',''),(16,'url/video/3gpp',''),(17,'url/video/mp4','H.263,H.264'),(18,'url/application/pdf',''),(19,'url/image/gif',''),(20,'url/web/other','');
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
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-05-27 10:31:25.847971','1','Blynq Pvt Ltd',1,'',17,1),(2,'2016-05-27 10:32:22.970936','1','manager',1,'',18,1),(3,'2016-05-27 10:32:28.288885','2','nipun',1,'',4,1),(4,'2016-05-27 10:33:07.503182','2','nipun',2,'Changed first_name, last_name, email, is_staff, is_superuser and last_login. Changed mobile_number for user details \"nipun\".',4,1),(5,'2016-05-28 13:20:32.220445','1','serial number android emulator jay key a197cb391f0698e5',1,'',23,1),(6,'2016-05-28 13:23:46.603616','1','Online',1,'',21,1),(7,'2016-05-28 13:34:14.115958','2','Offline',1,'',21,1),(8,'2016-05-29 10:35:23.672811','1','Hyderabad, Telangana',1,'',15,1),(9,'2016-05-29 10:35:54.757843','2','Visakhapatnam, Andhra Pradesh',1,'',15,1),(10,'2016-05-29 10:36:32.719708','1','jaydev android emulator',2,'Changed city.',26,1),(11,'2016-05-29 11:04:13.293057','1','Group 1',1,'',24,1),(12,'2016-05-29 11:04:55.817976','1','jaydev android emulator-Group 1',1,'',25,1),(13,'2016-05-29 11:41:35.631796','2','Group 2',1,'',24,1),(14,'2016-05-29 11:45:24.717899','2','serial number abc def key 1234567890',1,'',23,1),(15,'2016-05-29 11:47:05.962391','2','test calendar',1,'',7,1),(16,'2016-05-29 11:47:08.864510','2','test',1,'',26,1),(17,'2016-05-29 14:31:29.948299','2','First schedule',1,'',33,1),(18,'2016-05-29 14:31:38.563753','1','first schedule',3,'',33,1),(19,'2016-05-29 14:32:34.758236','1','first event: May 29, 2016 - May 29, 2016',1,'',10,1),(21,'2016-05-29 14:32:50.123950','2','First schedule-first playlist',1,'',32,1),(23,'2016-05-29 14:59:55.860252','2','test: May 29, 2016 - May 29, 2016',1,'',10,1),(25,'2016-05-29 20:11:31.452390','3','temp1',3,'',33,1),(42,'2016-06-09 13:58:17.230206','23','123: June 9, 2016 - June 9, 2016',1,'',10,2),(43,'2016-06-09 13:58:28.056642','23','123: June 9, 2016 - June 9, 2016',3,'',10,2),(47,'2016-06-09 14:06:22.746284','11','6',3,'',33,2),(48,'2016-06-09 14:07:07.880128','6','First schedule: May 30, 2016 - May 30, 2016',3,'',10,2),(49,'2016-06-09 14:07:07.884498','5','4: May 30, 2016 - May 30, 2016',3,'',10,2),(50,'2016-06-09 14:07:07.888121','4','2: May 30, 2016 - May 30, 2016',3,'',10,2),(51,'2016-06-09 14:07:07.899246','3','1: May 30, 2016 - May 30, 2016',3,'',10,2),(52,'2016-06-09 14:07:07.902985','2','First schedule: May 30, 2016 - May 30, 2016',3,'',10,2),(53,'2016-06-09 14:07:20.443247','9','Rule First schedule params None',3,'',9,2),(54,'2016-06-09 14:07:20.454568','8','Rule 4 params None',3,'',9,2),(55,'2016-06-09 14:07:20.459168','4','Rule 2 params None',3,'',9,2),(56,'2016-06-09 14:07:20.463799','3','Rule 1 params None',3,'',9,2),(57,'2016-06-09 14:07:20.471600','2','Rule temp1 params None',3,'',9,2),(58,'2016-06-10 14:57:40.200737','2','iframe',1,'',35,2),(59,'2016-06-10 14:58:01.732566','3','url',1,'',35,2),(60,'2016-06-10 14:58:52.995560','4','image/gif',1,'',35,2),(61,'2016-06-10 15:00:03.665196','5','application/pdf',1,'',35,2),(62,'2016-06-10 15:00:58.728984','6','video/mp4',1,'',35,2),(63,'2016-06-10 15:01:18.432069','7','video/3gpp',1,'',35,2),(64,'2016-06-10 15:02:06.875513','8','image/jpeg',1,'',35,2),(65,'2016-06-10 15:03:21.432353','9','image/png',1,'',35,2),(66,'2016-06-10 15:04:28.454380','10','image/bmp',1,'',35,2),(67,'2016-06-10 15:04:56.422690','11','image/webp',1,'',35,2),(68,'2016-06-12 06:40:45.602182','12','url/image/webp',1,'',35,2),(69,'2016-06-12 06:41:01.195957','13','url/image/jpeg',1,'',35,2),(70,'2016-06-12 06:41:13.788429','14','url/image/bmp',1,'',35,2),(71,'2016-06-12 06:41:19.866346','15','url/image/png',1,'',35,2),(72,'2016-06-12 06:41:35.061763','16','url/video/3gpp',1,'',35,2),(73,'2016-06-12 06:41:46.690387','17','url/video/mp4',1,'',35,2),(74,'2016-06-12 06:41:59.617993','18','url/application/pdf',1,'',35,2),(75,'2016-06-12 06:42:22.927594','17','url/video/mp4',2,'Changed supported_encodings.',35,2),(76,'2016-06-12 06:42:32.744183','19','url/image/gif',1,'',35,2),(77,'2016-06-13 09:27:54.544887','11','file/image/webp',2,'Changed file_type.',35,2),(78,'2016-06-13 09:28:01.766896','10','file/image/bmp',2,'Changed file_type.',35,2),(79,'2016-06-13 09:28:10.492672','9','file/image/png',2,'Changed file_type.',35,2),(80,'2016-06-13 09:28:17.332843','8','file/image/jpeg',2,'Changed file_type.',35,2),(81,'2016-06-13 09:28:23.854696','7','file/video/3gpp',2,'Changed file_type.',35,2),(82,'2016-06-13 09:28:32.411641','6','file/video/mp4',2,'Changed file_type.',35,2),(83,'2016-06-13 09:28:39.914207','5','file/application/pdf',2,'Changed file_type.',35,2),(84,'2016-06-13 09:28:47.934610','4','file/image/gif',2,'Changed file_type.',35,2),(85,'2016-06-13 09:28:56.175377','3','web/url',2,'Changed file_type.',35,2),(86,'2016-06-13 09:29:03.201775','2','web/iframe',2,'Changed file_type.',35,2),(89,'2016-06-27 16:59:31.707831','3','web/url/youtube',2,'Changed file_type.',35,2),(90,'2016-06-27 16:59:41.755191','20','web/url/unknown',1,'',35,2),(91,'2016-06-27 17:00:16.712065','8','file/image/jpeg',2,'No fields changed.',35,2),(92,'2016-06-27 17:00:22.875117','21','file/image/jpg',1,'',35,2),(93,'2016-06-27 17:06:15.803808','22','url/image/jpg',1,'',35,2),(94,'2016-06-27 17:35:23.563944','22','url/image/jpg',3,'',35,2),(95,'2016-06-27 17:35:23.576129','21','file/image/jpg',3,'',35,2),(96,'2016-06-28 04:52:06.412813','20','url/web/unknown',2,'Changed file_type.',35,2),(97,'2016-06-28 04:52:17.770023','3','url/web/youtube',2,'Changed file_type.',35,2),(98,'2016-06-28 04:52:32.871729','2','url/web/iframe',2,'Changed file_type.',35,2),(99,'2016-06-28 04:55:53.373461','20','url/web/other',2,'Changed file_type.',35,2),(100,'2016-06-29 10:36:20.483718','1','Blynq Pvt Ltd',2,'Changed used_file_size.',17,2),(124,'2016-07-15 13:00:10.613024','23','11',2,'Changed split_screen.',33,2),(125,'2016-07-19 08:11:36.528469','1','serial number android emulator jay key a197cb391f0698e5',2,'Changed verified.',23,2),(131,'2016-07-26 17:53:25.689495','1','AspectRatio object',1,'',48,2),(132,'2016-07-26 18:07:58.078412','2','4:3 Portrait',1,'',48,2),(133,'2016-07-26 18:08:57.571995','3','16:9 Landscape',1,'',48,2),(134,'2016-07-26 18:09:14.602249','4','16:9 Portrait',1,'',48,2),(135,'2016-07-26 18:09:22.459977','3','16:9 Landscape',2,'No fields changed.',48,2),(136,'2016-07-26 21:17:26.098595','1','Full Screen',1,'',50,2),(137,'2016-07-26 21:22:33.167865','1','Full Screen-Full Screen Pane',1,'',49,2),(138,'2016-07-26 21:22:47.944936','1','Full Screen-Pane 0',2,'Changed title.',49,2);
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(15,'authentication','city'),(17,'authentication','organization'),(20,'authentication','requestedquote'),(18,'authentication','role'),(19,'authentication','userdetails'),(28,'contentManagement','content'),(35,'contentManagement','contenttype'),(5,'contenttypes','contenttype'),(50,'layoutManagement','layout'),(49,'layoutManagement','layoutpane'),(39,'playerManagement','localserver'),(38,'playerManagement','playerupdate'),(30,'playlistManagement','playlist'),(29,'playlistManagement','playlistitems'),(13,'reversion','revision'),(14,'reversion','version'),(7,'schedule','calendar'),(8,'schedule','calendarrelation'),(10,'schedule','event'),(11,'schedule','eventrelation'),(12,'schedule','occurrence'),(9,'schedule','rule'),(33,'scheduleManagement','schedule'),(46,'scheduleManagement','schedulepane'),(32,'scheduleManagement','scheduleplaylists'),(47,'scheduleManagement','schedulescreens'),(48,'screenManagement','aspectratio'),(24,'screenManagement','group'),(25,'screenManagement','groupscreens'),(26,'screenManagement','screen'),(23,'screenManagement','screenactivationkey'),(21,'screenManagement','screenstatus'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-05-27 10:26:10.049497'),(2,'auth','0001_initial','2016-05-27 10:26:10.689228'),(3,'admin','0001_initial','2016-05-27 10:26:10.844101'),(4,'contenttypes','0002_remove_content_type_name','2016-05-27 10:26:10.973854'),(5,'auth','0002_alter_permission_name_max_length','2016-05-27 10:26:11.043031'),(6,'auth','0003_alter_user_email_max_length','2016-05-27 10:26:11.103787'),(7,'auth','0004_alter_user_username_opts','2016-05-27 10:26:11.124732'),(8,'auth','0005_alter_user_last_login_null','2016-05-27 10:26:11.186766'),(9,'auth','0006_require_contenttypes_0002','2016-05-27 10:26:11.191124'),(10,'authentication','0001_initial','2016-05-27 10:26:11.936689'),(11,'contentManagement','0001_initial','2016-05-27 10:26:12.222907'),(12,'playlistManagement','0001_initial','2016-05-27 10:26:12.635050'),(13,'reversion','0001_initial','2016-05-27 10:26:12.974337'),(14,'reversion','0002_auto_20141216_1509','2016-05-27 10:26:13.084752'),(15,'schedule','0001_initial','2016-05-27 10:26:13.958068'),(16,'screenManagement','0001_initial','2016-05-27 10:26:15.357763'),(17,'scheduleManagement','0001_initial','2016-05-27 10:26:15.560291'),(18,'scheduleManagement','0002_auto_20160527_1025','2016-05-27 10:26:17.312932'),(19,'sessions','0001_initial','2016-05-27 10:26:17.381577'),(20,'screenManagement','0002_auto_20160528_1336','2016-05-28 13:36:20.494814'),(21,'screenManagement','0003_auto_20160529_0716','2016-05-29 07:17:14.980089'),(22,'screenManagement','0004_screen_city','2016-05-29 07:42:54.651276'),(23,'authentication','0002_auto_20160529_1050','2016-05-29 10:50:15.868640'),(24,'contentManagement','0002_auto_20160531_0559','2016-05-31 05:59:12.510681'),(25,'screenManagement','0005_auto_20160601_1412','2016-06-02 04:28:57.388413'),(26,'screenManagement','0006_delete_screenspecs','2016-06-02 04:28:57.454790'),(27,'authentication','0003_auto_20160602_0707','2016-06-02 07:07:38.114507'),(28,'authentication','0004_auto_20160603_0655','2016-06-03 06:55:16.124173'),(29,'screenManagement','0007_auto_20160603_1056','2016-06-03 10:56:15.707209'),(30,'contentManagement','0003_delete_contenttype','2016-06-04 11:38:28.912221'),(31,'playlistManagement','0002_auto_20160604_1138','2016-06-04 11:38:28.981929'),(32,'contentManagement','0004_contenttype','2016-06-04 15:29:04.691309'),(33,'playlistManagement','0003_auto_20160604_1529','2016-06-04 15:29:04.739242'),(34,'contentManagement','0005_delete_contenttype','2016-06-06 07:17:04.830071'),(35,'playlistManagement','0004_auto_20160606_0717','2016-06-06 07:17:04.929096'),(36,'contentManagement','0006_auto_20160610_1418','2016-06-10 14:48:41.031483'),(37,'contentManagement','0007_auto_20160610_1448','2016-06-10 14:48:41.527073'),(38,'playlistManagement','0005_auto_20160610_1418','2016-06-10 14:48:41.593644'),(39,'scheduleManagement','0003_auto_20160610_1418','2016-06-10 14:48:41.670834'),(40,'contentManagement','0008_auto_20160610_1456','2016-06-10 14:56:14.647458'),(41,'contentManagement','0009_auto_20160610_1459','2016-06-10 14:59:49.870795'),(42,'contentManagement','0010_remove_contenttype_category','2016-06-12 06:40:08.760925'),(43,'authentication','0005_localserver','2016-06-13 13:28:05.732434'),(44,'authentication','0006_auto_20160614_1056','2016-06-14 10:56:38.244002'),(45,'screenManagement','0008_auto_20160614_1114','2016-06-14 11:17:52.537038'),(46,'screenManagement','0009_auto_20160614_1117','2016-06-14 11:17:52.867429'),(47,'authentication','0006_auto_20160627_0620','2016-06-27 06:20:31.446323'),(48,'authentication','0007_merge','2016-06-27 06:36:38.730975'),(49,'authentication','0008_playerupdate','2016-07-03 06:00:08.092157'),(50,'contentManagement','0011_auto_20160703_0559','2016-07-03 06:00:08.141404'),(51,'authentication','0009_auto_20160706_1645','2016-07-06 16:53:10.519437'),(52,'playerManagement','0001_initial','2016-07-06 16:53:10.780297'),(53,'screenManagement','0010_splitscreen','2016-07-08 19:06:51.486695'),(54,'screenManagement','0011_auto_20160708_1906','2016-07-08 19:06:52.201522'),(55,'scheduleManagement','0004_auto_20160708_1906','2016-07-08 19:06:56.425844'),(56,'screenManagement','0012_auto_20160709_0450','2016-07-09 04:50:17.915610'),(57,'screenManagement','0013_auto_20160709_1717','2016-07-09 17:17:29.412919'),(58,'scheduleManagement','0005_auto_20160709_1717','2016-07-09 17:17:31.950351'),(59,'scheduleManagement','0006_auto_20160709_1754','2016-07-09 17:54:36.454030'),(60,'screenManagement','0014_auto_20160709_1754','2016-07-09 17:54:37.363502'),(61,'scheduleManagement','0007_auto_20160709_1821','2016-07-09 18:21:38.932824'),(62,'scheduleManagement','0008_auto_20160715_1240','2016-07-15 12:45:12.324172'),(63,'scheduleManagement','0009_auto_20160715_1241','2016-07-15 12:45:12.565187'),(64,'screenManagement','0015_remove_splitscreen_layout_id','2016-07-15 12:49:47.713029'),(65,'scheduleManagement','0010_remove_schedulescreens_event','2016-07-19 06:38:26.534755'),(66,'screenManagement','0016_auto_20160719_0638','2016-07-19 06:38:26.751350'),(67,'layoutManagement','0001_initial','2016-07-26 17:48:20.635691'),(68,'scheduleManagement','0011_auto_20160726_1748','2016-07-26 17:48:21.707692'),(69,'screenManagement','0017_auto_20160726_1748','2016-07-26 17:48:21.890945'),(70,'layoutManagement','0002_layout_aspect_ratio','2016-07-26 17:48:22.092637'),(71,'screenManagement','0018_aspectratio_orientation','2016-07-26 18:05:34.733329'),(72,'layoutManagement','0003_layout_organization','2016-07-26 18:24:48.495712'),(73,'layoutManagement','0004_auto_20160726_1943','2016-07-26 19:43:17.500154'),(74,'authentication','0010_auto_20160728_0258','2016-07-28 02:59:36.397438'),(75,'screenManagement','0019_screen_last_active_time','2016-07-28 02:59:36.710715'),(76,'screenManagement','0020_auto_20160728_0320','2016-07-28 03:20:23.683766');
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
INSERT INTO `django_session` VALUES ('5e5i0anb1nay4n7cflfv5f8f2gjlmsl6','MDU1MzdmYjBmZjBmNzliNTMyNDAwODIxMDM4ZTcxOWIxMjZjYmM3Njp7Il9hdXRoX3VzZXJfaGFzaCI6IjZlNDViNGNiNTMzMjYzMzEzMjdkMGE2ZDE3ZjZlMWFiN2I0NzUyNWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2016-06-27 18:41:51.225659'),('ohwzle6fm691xoput26cfss8xl1qycil','MDU1MzdmYjBmZjBmNzliNTMyNDAwODIxMDM4ZTcxOWIxMjZjYmM3Njp7Il9hdXRoX3VzZXJfaGFzaCI6IjZlNDViNGNiNTMzMjYzMzEzMjdkMGE2ZDE3ZjZlMWFiN2I0NzUyNWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2016-07-27 06:50:02.893491'),('pr961azwedk5xztkmu09oc1v4ob1q5qw','MDU1MzdmYjBmZjBmNzliNTMyNDAwODIxMDM4ZTcxOWIxMjZjYmM3Njp7Il9hdXRoX3VzZXJfaGFzaCI6IjZlNDViNGNiNTMzMjYzMzEzMjdkMGE2ZDE3ZjZlMWFiN2I0NzUyNWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2016-08-11 03:22:40.897101'),('wlis11yf4yh7yptlluharf3sqm0nif5l','MDU1MzdmYjBmZjBmNzliNTMyNDAwODIxMDM4ZTcxOWIxMjZjYmM3Njp7Il9hdXRoX3VzZXJfaGFzaCI6IjZlNDViNGNiNTMzMjYzMzEzMjdkMGE2ZDE3ZjZlMWFiN2I0NzUyNWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2016-07-12 05:22:46.950130');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `layoutManagement_layout`
--

DROP TABLE IF EXISTS `layoutManagement_layout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `layoutManagement_layout` (
  `layout_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `aspect_ratio_id` int(11),
  `organization_id` int(11),
  PRIMARY KEY (`layout_id`),
  KEY `layoutManagement_layout_c7ddd106` (`aspect_ratio_id`),
  KEY `layoutManagement_layout_26b2345e` (`organization_id`),
  CONSTRAINT `D599719009109dcfcd989cf604f104c0` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `cd03f13f5ddd422a9cefbd23ebda3370` FOREIGN KEY (`aspect_ratio_id`) REFERENCES `screenManagement_aspectratio` (`aspect_ratio_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layoutManagement_layout`
--

LOCK TABLES `layoutManagement_layout` WRITE;
/*!40000 ALTER TABLE `layoutManagement_layout` DISABLE KEYS */;
INSERT INTO `layoutManagement_layout` VALUES (1,'Full Screen',1,3,NULL),(2,'New layout',0,1,1);
/*!40000 ALTER TABLE `layoutManagement_layout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `layoutManagement_layoutpane`
--

DROP TABLE IF EXISTS `layoutManagement_layoutpane`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `layoutManagement_layoutpane` (
  `layout_pane_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `left_margin` int(10) unsigned NOT NULL,
  `top_margin` int(10) unsigned NOT NULL,
  `z_index` int(11) NOT NULL,
  `width` int(10) unsigned NOT NULL,
  `height` int(10) unsigned NOT NULL,
  `layout_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`layout_pane_id`),
  KEY `l_layout_id_2fc831f3bed8a4d_fk_layoutManagement_layout_layout_id` (`layout_id`),
  CONSTRAINT `l_layout_id_2fc831f3bed8a4d_fk_layoutManagement_layout_layout_id` FOREIGN KEY (`layout_id`) REFERENCES `layoutManagement_layout` (`layout_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `layoutManagement_layoutpane`
--

LOCK TABLES `layoutManagement_layoutpane` WRITE;
/*!40000 ALTER TABLE `layoutManagement_layoutpane` DISABLE KEYS */;
INSERT INTO `layoutManagement_layoutpane` VALUES (1,'Pane 0',0,0,0,100,100,1),(2,'Pane0',0,0,0,52,59,2),(3,'Pane1',66,12,1,33,47,2);
/*!40000 ALTER TABLE `layoutManagement_layoutpane` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playerManagement_localserver`
--

DROP TABLE IF EXISTS `playerManagement_localserver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playerManagement_localserver` (
  `local_server_id` int(11) NOT NULL AUTO_INCREMENT,
  `local_url` varchar(255) NOT NULL,
  `unique_key` varchar(20) NOT NULL,
  `organization_id` int(11) NOT NULL,
  PRIMARY KEY (`local_server_id`),
  KEY `D4d126045ade6d0a62ebe8cbbc177bfb` (`organization_id`),
  CONSTRAINT `D4d126045ade6d0a62ebe8cbbc177bfb` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playerManagement_localserver`
--

LOCK TABLES `playerManagement_localserver` WRITE;
/*!40000 ALTER TABLE `playerManagement_localserver` DISABLE KEYS */;
/*!40000 ALTER TABLE `playerManagement_localserver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playerManagement_playerupdate`
--

DROP TABLE IF EXISTS `playerManagement_playerupdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playerManagement_playerupdate` (
  `player_update_id` int(11) NOT NULL AUTO_INCREMENT,
  `executable` varchar(100) NOT NULL,
  `comments` longtext,
  `uploaded_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `uploaded_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`player_update_id`),
  KEY `D020b61a66fa0962253dae6e82b83886` (`uploaded_by_id`),
  CONSTRAINT `D020b61a66fa0962253dae6e82b83886` FOREIGN KEY (`uploaded_by_id`) REFERENCES `authentication_userdetails` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playerManagement_playerupdate`
--

LOCK TABLES `playerManagement_playerupdate` WRITE;
/*!40000 ALTER TABLE `playerManagement_playerupdate` DISABLE KEYS */;
/*!40000 ALTER TABLE `playerManagement_playerupdate` ENABLE KEYS */;
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
  `playlist_total_time` int(11),
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `last_updated_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `created_by_id_22fae803a698f2ed_fk_authentication_userdetails_id` (`created_by_id`),
  KEY `e90b89de965486e2a427c97ae59dcba9` (`last_updated_by_id`),
  KEY `D9f916f791b6ae8d4fd6a9f347b63d4b` (`organization_id`),
  CONSTRAINT `D9f916f791b6ae8d4fd6a9f347b63d4b` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `created_by_id_22fae803a698f2ed_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `e90b89de965486e2a427c97ae59dcba9` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlist`
--

LOCK TABLES `playlistManagement_playlist` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlist` DISABLE KEYS */;
INSERT INTO `playlistManagement_playlist` VALUES (1,'first playlist',30,'2016-05-29 13:06:52.524586','2016-06-23 10:29:19.421362',1,1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlistitems`
--

LOCK TABLES `playlistManagement_playlistitems` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlistitems` DISABLE KEYS */;
INSERT INTO `playlistManagement_playlistitems` VALUES (7,0,15,11,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_revision`
--

LOCK TABLES `reversion_revision` WRITE;
/*!40000 ALTER TABLE `reversion_revision` DISABLE KEYS */;
INSERT INTO `reversion_revision` VALUES (1,'default','2016-05-27 10:29:38.108787','',1),(2,'default','2016-05-27 10:31:25.863484','Initial version.',1),(3,'default','2016-05-27 10:32:28.318508','Initial version.',1),(4,'default','2016-05-27 10:33:07.521794','Changed first_name, last_name, email, is_staff, is_superuser and last_login. Changed mobile_number for user details \"nipun\".',1),(5,'default','2016-05-27 10:33:37.728837','',2),(6,'default','2016-05-28 13:16:23.718135','',2),(7,'default','2016-05-28 13:20:05.299312','',1),(8,'default','2016-05-28 13:36:27.266907','',2),(9,'default','2016-05-29 10:36:32.905106','Changed city.',1),(10,'default','2016-05-29 11:04:13.463652','Initial version.',1),(11,'default','2016-05-29 11:04:55.823768','Initial version.',1),(12,'default','2016-05-29 11:41:35.813753','Initial version.',1),(13,'default','2016-05-29 11:47:09.042238','Initial version.',1),(14,'default','2016-05-29 12:38:15.688195','',2),(15,'default','2016-05-29 12:38:25.479914','',2),(16,'default','2016-05-29 13:06:52.795248','',2),(17,'default','2016-05-29 13:07:01.476722','',2),(18,'default','2016-05-29 13:07:06.481637','',2),(19,'default','2016-05-29 13:12:22.464073','',2),(20,'default','2016-05-29 13:12:35.492765','',2),(21,'default','2016-05-29 13:54:29.440872','',2),(22,'default','2016-05-29 13:55:01.442131','',2),(23,'default','2016-05-29 14:17:25.437525','',2),(24,'default','2016-05-29 14:31:29.956282','Initial version.',1),(25,'default','2016-05-29 14:32:37.614493','Initial version.',1),(26,'default','2016-05-29 14:32:50.128573','Initial version.',1),(27,'default','2016-05-29 14:52:26.344940','Changed group.',1),(28,'default','2016-05-29 14:59:58.040854','Initial version.',1),(29,'default','2016-05-29 20:11:20.178482','',2),(30,'default','2016-05-30 18:58:38.678561','',2),(31,'default','2016-05-30 20:10:36.184391','',2),(32,'default','2016-05-30 20:13:18.837271','',2),(33,'default','2016-05-30 20:14:16.641664','',2),(34,'default','2016-05-30 20:15:02.785046','',2),(35,'default','2016-05-30 20:37:09.502075','',2),(36,'default','2016-05-30 21:15:33.534795','',2),(37,'default','2016-05-31 04:37:34.395124','',2),(38,'default','2016-05-31 04:39:13.705697','',2),(39,'default','2016-05-31 04:39:50.347624','',2),(40,'default','2016-05-31 12:32:37.698377','',2),(41,'default','2016-05-31 13:16:43.786608','',2),(42,'default','2016-05-31 13:16:52.273675','',2),(43,'default','2016-05-31 13:19:43.311474','',2),(44,'default','2016-05-31 13:19:49.503999','',2),(45,'default','2016-05-31 13:21:49.593495','',2),(46,'default','2016-05-31 13:22:44.300674','',2),(47,'default','2016-05-31 15:39:22.049745','',2),(48,'default','2016-05-31 15:39:54.248205','',2),(49,'default','2016-05-31 19:34:07.918609','',2),(50,'default','2016-05-31 19:34:21.136919','',2),(51,'default','2016-05-31 19:38:11.325137','',2),(52,'default','2016-05-31 19:38:20.574437','',2),(53,'default','2016-05-31 19:39:58.643681','',2),(54,'default','2016-05-31 19:40:11.076646','',2),(55,'default','2016-06-01 12:49:49.255644','',2),(56,'default','2016-06-01 12:50:07.803059','',2),(57,'default','2016-06-01 12:50:16.458600','',2),(58,'default','2016-06-01 12:50:30.584611','',2),(59,'default','2016-06-04 12:04:06.318760','',2),(60,'default','2016-06-04 12:05:53.968557','',2),(61,'default','2016-06-05 07:00:30.623779','',2),(62,'default','2016-06-05 07:00:42.854937','',2),(63,'default','2016-06-05 07:00:46.532556','',2),(64,'default','2016-06-05 07:38:49.074505','',2),(65,'default','2016-06-05 07:47:34.790294','',2),(66,'default','2016-06-05 07:48:11.709683','',2),(67,'default','2016-06-05 07:50:14.184110','',2),(68,'default','2016-06-05 08:17:17.484156','',2),(69,'default','2016-06-05 10:23:24.101391','',2),(70,'default','2016-06-07 20:20:15.405642','',2),(71,'default','2016-06-08 13:22:26.887200','',2),(72,'default','2016-06-09 05:54:49.472209','',2),(73,'default','2016-06-09 12:01:57.809879','',2),(74,'default','2016-06-09 13:42:04.614904','',2),(75,'default','2016-06-09 14:08:50.350263','',2),(76,'default','2016-06-09 14:09:24.504230','',2),(77,'default','2016-06-09 14:13:19.788392','',2),(78,'default','2016-06-09 14:15:15.363562','',2),(79,'default','2016-06-09 14:23:17.925108','',2),(80,'default','2016-06-09 14:24:21.637092','',2),(81,'default','2016-06-09 14:25:19.096979','',2),(82,'default','2016-06-09 14:25:55.398770','',2),(83,'default','2016-06-09 20:21:29.516927','',2),(84,'default','2016-06-09 20:31:49.812086','',2),(85,'default','2016-06-09 20:32:11.594044','',2),(86,'default','2016-06-09 20:32:19.249510','',2),(87,'default','2016-06-09 20:32:39.334700','',2),(88,'default','2016-06-09 20:40:56.866504','',2),(89,'default','2016-06-09 20:41:12.319758','',2),(90,'default','2016-06-09 20:41:50.003778','',2),(91,'default','2016-06-09 20:42:11.809352','',2),(92,'default','2016-06-09 21:02:55.745686','',2),(93,'default','2016-06-13 10:55:12.086687','',2),(94,'default','2016-06-13 18:41:51.562577','',2),(95,'default','2016-06-13 18:42:16.731907','',2),(96,'default','2016-06-23 06:21:53.546707','',2),(97,'default','2016-06-23 08:00:27.215386','',2),(98,'default','2016-06-23 08:01:31.229001','',2),(99,'default','2016-06-23 08:01:41.801517','',2),(100,'default','2016-06-23 08:04:11.642454','',2),(101,'default','2016-06-23 08:04:16.281961','',2),(102,'default','2016-06-23 08:40:49.358851','',2),(103,'default','2016-06-23 08:40:56.314562','',2),(104,'default','2016-06-23 09:14:12.300475','',2),(105,'default','2016-06-23 09:14:26.034146','',2),(106,'default','2016-06-23 09:16:20.568975','',2),(107,'default','2016-06-23 09:18:21.957230','',2),(108,'default','2016-06-23 10:23:23.402128','',2),(109,'default','2016-06-23 10:23:43.902477','',2),(110,'default','2016-06-23 10:23:56.637419','',2),(111,'default','2016-06-23 10:24:32.621043','',2),(112,'default','2016-06-23 10:27:40.899674','',2),(113,'default','2016-06-23 10:28:56.786593','',2),(114,'default','2016-06-23 10:29:12.211434','',2),(115,'default','2016-06-23 10:29:19.458613','',2),(116,'default','2016-06-27 12:12:11.372584','',2),(117,'default','2016-06-27 12:13:04.267311','',2),(118,'default','2016-06-27 13:51:06.640320','',2),(119,'default','2016-06-27 14:22:31.347106','',2),(120,'default','2016-06-27 14:23:29.692582','',2),(121,'default','2016-06-27 14:36:26.293989','',2),(122,'default','2016-06-27 14:49:03.592864','',2),(123,'default','2016-06-27 18:11:21.535124','',2),(124,'default','2016-06-28 04:51:48.901830','',2),(125,'default','2016-06-28 05:22:47.127314','',2),(126,'default','2016-06-28 08:08:43.599559','',2),(127,'default','2016-06-28 08:12:24.690498','',2),(128,'default','2016-06-28 08:14:02.197708','',2),(129,'default','2016-06-28 08:14:12.890433','',2),(130,'default','2016-06-28 08:15:53.305959','',2),(131,'default','2016-06-29 10:36:20.493635','Changed used_file_size.',2),(132,'default','2016-06-29 13:28:07.615962','',2),(133,'default','2016-06-29 13:28:15.287839','',2),(134,'default','2016-07-02 19:34:36.636392','',2),(135,'default','2016-07-02 19:35:18.161638','',2),(136,'default','2016-07-02 19:35:46.628223','',2),(137,'default','2016-07-02 19:38:50.804048','',2),(138,'default','2016-07-02 19:43:36.781047','',2),(139,'default','2016-07-02 19:43:53.237428','',2),(140,'default','2016-07-02 19:44:02.320788','',2),(141,'default','2016-07-02 19:44:23.482899','',2),(142,'default','2016-07-02 19:58:20.817766','',2),(143,'default','2016-07-02 20:01:58.310732','',2),(144,'default','2016-07-02 20:02:01.042260','',2),(145,'default','2016-07-02 20:03:02.738810','',2),(146,'default','2016-07-02 20:07:25.929538','',2),(147,'default','2016-07-02 20:08:16.751233','',2),(148,'default','2016-07-02 20:10:58.009997','',2),(149,'default','2016-07-02 20:22:38.755412','',2),(150,'default','2016-07-02 20:22:45.735729','',2),(151,'default','2016-07-02 20:23:31.125827','',2),(152,'default','2016-07-02 20:27:32.929274','',2),(153,'default','2016-07-02 20:28:13.393501','',2),(154,'default','2016-07-02 20:29:49.576857','',2),(155,'default','2016-07-02 20:30:37.103033','',2),(156,'default','2016-07-05 08:17:14.958212','',2),(157,'default','2016-07-05 08:32:45.047785','',2),(158,'default','2016-07-05 08:32:47.690395','',2),(159,'default','2016-07-05 08:34:08.833152','',2),(160,'default','2016-07-13 06:50:03.121232','',2),(161,'default','2016-07-15 07:36:02.086482','',2),(162,'default','2016-07-15 07:44:29.541066','',2),(163,'default','2016-07-15 07:50:06.436385','',2),(164,'default','2016-07-15 07:56:39.852224','',2),(165,'default','2016-07-15 09:43:00.522496','',2),(166,'default','2016-07-15 13:00:10.767095','Changed split_screen.',2),(167,'default','2016-07-19 08:27:29.771319','',2),(168,'default','2016-07-20 15:27:58.085211','',2),(169,'default','2016-07-20 16:13:12.730451','',2),(170,'default','2016-07-28 03:22:41.084370','',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=385 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_version`
--

LOCK TABLES `reversion_version` WRITE;
/*!40000 ALTER TABLE `reversion_version` DISABLE KEYS */;
INSERT INTO `reversion_version` VALUES (1,'1',1,'json','[{\"fields\": {\"username\": \"admin\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:29:37.895Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=\", \"email\": \"hello@blynq.in\", \"date_joined\": \"2016-05-27T10:29:30.217Z\"}, \"model\": \"auth.user\", \"pk\": 1}]','admin',4,1),(2,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 0, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,2),(3,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"8277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,3),(4,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": null, \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"\", \"date_joined\": \"2016-05-27T10:32:28.226Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,3),(5,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,4),(6,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:33:02Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,4),(7,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,5),(8,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:33:37.691Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,5),(9,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,6),(10,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-28T13:16:23.455Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,6),(11,'1',1,'json','[{\"fields\": {\"username\": \"admin\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-28T13:20:05.178Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=\", \"email\": \"hello@blynq.in\", \"date_joined\": \"2016-05-27T10:29:30.217Z\"}, \"model\": \"auth.user\", \"pk\": 1}]','admin',4,7),(12,'1',1,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 2, \"activated_by\": 1, \"screen_name\": \"jaydev android emulator\", \"screen_calendar\": 1, \"screen_size\": 32, \"address\": \"\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 1, \"resolution\": \"1190*768\", \"activated_on\": \"2016-05-28T13:36:27.202Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 1}]','jaydev android emulator',26,8),(13,'1',1,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"jaydev android emulator\", \"screen_calendar\": 1, \"screen_size\": 32, \"status\": 2, \"address\": \"\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 1, \"resolution\": \"1190*768\", \"activated_on\": \"2016-05-28T13:36:27.202Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 1}]','jaydev android emulator',26,9),(14,'1',1,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-29\", \"description\": \"First group\", \"created_by\": 1, \"group_name\": \"Group 1\"}, \"model\": \"screenManagement.group\", \"pk\": 1}]','Group 1',24,10),(15,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": 1, \"created_by\": 1}, \"model\": \"screenManagement.groupscreens\", \"pk\": 1}]','jaydev android emulator-Group 1',25,11),(16,'2',2,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-29\", \"description\": \"The second group\", \"created_by\": 1, \"group_name\": \"Group 2\"}, \"model\": \"screenManagement.group\", \"pk\": 2}]','Group 2',24,12),(17,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test',26,13),(18,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34373, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,14),(19,'1',1,'json','[{\"fields\": {\"document\": \"usercontent/1/fuck_you_bitches.jpg\", \"is_folder\": false, \"title\": \"fuck_you_bitches\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T12:38:15.549Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T12:38:15.550Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 1}]','fuck_you_bitches',28,14),(20,'2',2,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"temp folder\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T12:38:25.475Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T12:38:25.475Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 2}]','temp folder',28,15),(21,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-05-29T13:06:52.533Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,16),(22,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 15, \"last_updated_time\": \"2016-05-29T13:07:01.464Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,17),(23,'1',1,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 1}]','first playlist - fuck_you_bitches',29,17),(24,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:07:06.460Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,18),(25,'2',2,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 2}]','first playlist - fuck_you_bitches',29,18),(26,'1',1,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 1}]','first playlist - fuck_you_bitches',29,18),(27,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 308913, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,19),(28,'3',3,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T13:12:22.456Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T13:12:22.456Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 3}]','sachin',28,19),(29,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:12:35.462Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,20),(30,'3',3,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 3}]','first playlist - sachin',29,20),(31,'4',4,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 4}]','first playlist - sachin',29,20),(32,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 60, \"last_updated_time\": \"2016-05-29T13:54:29.187Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,21),(33,'3',3,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 3}]','first playlist - sachin',29,21),(34,'4',4,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 4}]','first playlist - sachin',29,21),(35,'5',5,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 2}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 5}]','first playlist - sachin',29,21),(36,'6',6,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 3}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 6}]','first playlist - fuck_you_bitches',29,21),(37,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:55:01.408Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,22),(38,'5',5,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 5}]','first playlist - sachin',29,22),(39,'6',6,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 6}]','first playlist - fuck_you_bitches',29,22),(40,'1',1,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T14:17:25.174Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:17:25.147Z\", \"organization\": 1, \"schedule_title\": \"first schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 1}]','first schedule',33,23),(41,'1',1,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 1}]','first schedule-first playlist',32,23),(42,'2',2,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T14:31:29.947Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:31:29.947Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 2}]','First schedule',33,24),(44,'2',2,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 1, \"schedule\": 2}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-first playlist',32,26),(47,'3',3,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T20:11:20.010Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T20:11:19.996Z\", \"organization\": 1, \"schedule_title\": \"temp1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 3}]','temp1',33,29),(48,'3',3,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 3}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 3}]','temp1-first playlist',32,29),(49,'4',4,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T18:58:38.471Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T18:58:38.426Z\", \"organization\": 1, \"schedule_title\": \"1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 4}]','1',33,30),(51,'4',4,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 4}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 4}]','1-first playlist',32,30),(53,'5',5,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:10:35.985Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:10:35.973Z\", \"organization\": 1, \"schedule_title\": \"2\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 5}]','2',33,31),(54,'5',5,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 5}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 5}]','2-first playlist',32,31),(55,'6',6,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:13:18.641Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:13:18.631Z\", \"organization\": 1, \"schedule_title\": \"3\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 6}]','3',33,32),(56,'6',6,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 6}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 6}]','3-first playlist',32,32),(57,'7',7,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:14:16.627Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:14:16.615Z\", \"organization\": 1, \"schedule_title\": \"3\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 7}]','3',33,33),(58,'7',7,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 7}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 7}]','3-first playlist',32,33),(59,'8',8,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:15:02.593Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:15:02.583Z\", \"organization\": 1, \"schedule_title\": \"4\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 8}]','4',33,34),(60,'8',8,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 8}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 8}]','4-first playlist',32,34),(61,'9',9,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:37:09.278Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:37:09.262Z\", \"organization\": 1, \"schedule_title\": \"4\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 9}]','4',33,35),(63,'9',9,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 9}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 9}]','4-first playlist',32,35),(65,'2',2,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T21:15:33.230Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:31:29.947Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 2}]','First schedule',33,36),(66,'2',2,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 2}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-first playlist',32,36),(68,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 314566, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,37),(69,'4',4,'json','[{\"fields\": {\"document\": \"usercontent/1/account_statement.pdf\", \"is_folder\": false, \"title\": \"account_statement\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T04:37:34.376Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:37:34.377Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"application/pdf\"}, \"model\": \"contentManagement.content\", \"pk\": 4}]','account_statement',28,37),(70,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 320219, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,38),(71,'4',4,'json','[{\"fields\": {\"document\": \"usercontent/1/account_statement.pdf\", \"is_folder\": false, \"title\": \"account_statement\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T04:37:34.376Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:39:13.700Z\", \"organization\": 1, \"parent_folder\": 2, \"document_type\": \"application/pdf\"}, \"model\": \"contentManagement.content\", \"pk\": 4}]','account_statement',28,38),(72,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 594759, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,39),(73,'3',3,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T13:12:22.456Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:39:50.341Z\", \"organization\": 1, \"parent_folder\": 2, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 3}]','sachin',28,39),(74,'10',10,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T12:32:37.528Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T12:32:37.509Z\", \"organization\": 1, \"schedule_title\": \"schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 10}]','schedule 1',33,40),(75,'10',10,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 10}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 10}]','schedule 1-first playlist',32,40),(78,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 43213, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,41),(79,'5',5,'json','[{\"fields\": {\"document\": \"usercontent/1/Virat.jpg\", \"is_folder\": false, \"title\": \"Virat\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:16:43.588Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:16:43.588Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 5}]','Virat',28,41),(80,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 1643880, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,42),(81,'6',6,'json','[{\"fields\": {\"document\": \"usercontent/1/Inspirational-Quotes-2.jpg\", \"is_folder\": false, \"title\": \"Inspirational-Quotes-2\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:16:52.263Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:16:52.263Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 6}]','Inspirational-Quotes-2',28,42),(82,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 1918420, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,43),(83,'7',7,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:19:43.120Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:19:43.120Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 7}]','sachin',28,43),(84,'8',8,'json','[{\"fields\": {\"document\": \"usercontent/1/when-throw-stones-sachin.jpg\", \"is_folder\": false, \"title\": \"when-throw-stones-sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:19:49.498Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:19:49.498Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 8}]','when-throw-stones-sachin',28,44),(85,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 1998946, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,44),(86,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 2273486, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,45),(87,'9',9,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:21:49.445Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:21:49.445Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 9}]','sachin',28,45),(88,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 2322377, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,46),(89,'10',10,'json','[{\"fields\": {\"document\": \"usercontent/1/francisofassisi121023.jpg\", \"is_folder\": false, \"title\": \"francisofassisi121023\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T13:22:44.128Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T13:22:44.128Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 10}]','francisofassisi121023',28,46),(91,'11',11,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T15:39:21.808Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T15:39:21.788Z\", \"organization\": 1, \"schedule_title\": \"6\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 11}]','6',33,47),(93,'11',11,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 11}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 11}]','6-first playlist',32,47),(97,'11',11,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:34:07.602Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T15:39:21.788Z\", \"organization\": 1, \"schedule_title\": \"6\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 11}]','6',33,49),(99,'11',11,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 11}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 11}]','6-first playlist',32,49),(101,'11',11,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:34:21.070Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T15:39:21.788Z\", \"organization\": 1, \"schedule_title\": \"6\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 11}]','6',33,50),(102,'11',11,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 11}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 11}]','6-first playlist',32,50),(105,'10',10,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:38:11.072Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T12:32:37.509Z\", \"organization\": 1, \"schedule_title\": \"schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 10}]','schedule 1',33,51),(107,'10',10,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 10}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 10}]','schedule 1-first playlist',32,51),(109,'10',10,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:38:20.518Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T12:32:37.509Z\", \"organization\": 1, \"schedule_title\": \"schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 10}]','schedule 1',33,52),(111,'10',10,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 10}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 10}]','schedule 1-first playlist',32,52),(114,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 2596917, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,53),(115,'11',11,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T19:39:58.628Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T19:39:58.628Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 11}]','sachin',28,53),(116,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 15, \"last_updated_time\": \"2016-05-31T19:40:11.053Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,54),(117,'10',10,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:40:11.062Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T12:32:37.509Z\", \"organization\": 1, \"schedule_title\": \"schedule 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 10}]','schedule 1',33,54),(118,'11',11,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-31T19:40:11.065Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-31T15:39:21.788Z\", \"organization\": 1, \"schedule_title\": \"6\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 11}]','6',33,54),(119,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,54),(120,'12',12,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"dude\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-01T12:49:49.034Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-01T12:49:49.035Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 12}]','dude',28,55),(121,'13',13,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"cheppu dude\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-01T12:50:07.790Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-01T12:50:07.790Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 13}]','cheppu dude',28,56),(122,'12',12,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"dude\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-01T12:49:49.034Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-01T12:50:16.449Z\", \"organization\": 1, \"parent_folder\": 13, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 12}]','dude',28,57),(123,'14',14,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"dude1\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-01T12:50:30.578Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-01T12:50:30.578Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 14}]','dude1',28,58),(124,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test',26,59),(125,'3',3,'json','[{\"fields\": {\"screen\": 2, \"group\": 1, \"created_by\": 1}, \"model\": \"screenManagement.groupscreens\", \"pk\": 3}]','test-Group 1',25,59),(128,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test',26,60),(129,'4',4,'json','[{\"fields\": {\"screen\": 2, \"group\": 1, \"created_by\": 1}, \"model\": \"screenManagement.groupscreens\", \"pk\": 4}]','test-Group 1',25,60),(130,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 4246475, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,61),(131,'12',12,'json','[{\"fields\": {\"document\": \"usercontent/1/francisofassisi121023.jpg\", \"is_folder\": false, \"title\": \"francisofassisi121023\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:00:30.422Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:00:30.422Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 12}]','francisofassisi121023',28,61),(132,'13',13,'json','[{\"fields\": {\"document\": \"usercontent/1/Inspirational-Quotes-2.jpg\", \"is_folder\": false, \"title\": \"Inspirational-Quotes-2\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:00:30.454Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:00:30.454Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 13}]','Inspirational-Quotes-2',28,61),(133,'14',14,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"first folder\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:00:42.849Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:00:42.849Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 14}]','first folder',28,62),(134,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 5847142, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,63),(135,'13',13,'json','[{\"fields\": {\"document\": \"usercontent/1/Inspirational-Quotes-2.jpg\", \"is_folder\": false, \"title\": \"Inspirational-Quotes-2\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:00:30.454Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:00:46.522Z\", \"organization\": 1, \"parent_folder\": 14, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 13}]','Inspirational-Quotes-2',28,63),(136,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 5881515, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,64),(137,'15',15,'json','[{\"fields\": {\"document\": \"usercontent/1/fuck_you_bitches.jpg\", \"is_folder\": false, \"title\": \"fuck_you_bitches\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:38:48.905Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:38:48.905Z\", \"organization\": 1, \"parent_folder\": 14, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 15}]','fuck_you_bitches',28,64),(138,'16',16,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"to be deleted\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:47:34.646Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:47:34.646Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"folder\"}, \"model\": \"contentManagement.content\", \"pk\": 16}]','to be deleted',28,65),(139,'32',32,'json','[{\"fields\": {\"document\": \"usercontent/user1/hyderabad-city-map.gif\", \"is_folder\": false, \"title\": \"hyderabad-city-map\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.689Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.689Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/gif\"}, \"model\": \"contentManagement.content\", \"pk\": 32}]','hyderabad-city-map',28,66),(140,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 8992191, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,66),(141,'17',17,'json','[{\"fields\": {\"document\": \"usercontent/user1/francisofassisi121023.jpg\", \"is_folder\": false, \"title\": \"francisofassisi121023\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.484Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.484Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 17}]','francisofassisi121023',28,66),(142,'18',18,'json','[{\"fields\": {\"document\": \"usercontent/user1/Inspirational-Quotes-2.jpg\", \"is_folder\": false, \"title\": \"Inspirational-Quotes-2\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.507Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.507Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 18}]','Inspirational-Quotes-2',28,66),(143,'19',19,'json','[{\"fields\": {\"document\": \"usercontent/user1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.522Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.523Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 19}]','sachin',28,66),(144,'20',20,'json','[{\"fields\": {\"document\": \"usercontent/user1/when-throw-stones-sachin.jpg\", \"is_folder\": false, \"title\": \"when-throw-stones-sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.534Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.534Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 20}]','when-throw-stones-sachin',28,66),(145,'21',21,'json','[{\"fields\": {\"document\": \"usercontent/user1/fuck_you_bitches.jpg\", \"is_folder\": false, \"title\": \"fuck_you_bitches\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.548Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.548Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 21}]','fuck_you_bitches',28,66),(146,'22',22,'json','[{\"fields\": {\"document\": \"usercontent/user1/Only logo blue.png\", \"is_folder\": false, \"title\": \"Only logo blue\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.564Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.564Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/png\"}, \"model\": \"contentManagement.content\", \"pk\": 22}]','Only logo blue',28,66),(147,'23',23,'json','[{\"fields\": {\"document\": \"usercontent/user1/Only logo white.png\", \"is_folder\": false, \"title\": \"Only logo white\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.576Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.576Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/png\"}, \"model\": \"contentManagement.content\", \"pk\": 23}]','Only logo white',28,66),(148,'24',24,'json','[{\"fields\": {\"document\": \"usercontent/user1/Virat.jpg\", \"is_folder\": false, \"title\": \"Virat\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.588Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.588Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 24}]','Virat',28,66),(149,'25',25,'json','[{\"fields\": {\"document\": \"usercontent/user1/jack-ma-quotes-5.jpg\", \"is_folder\": false, \"title\": \"jack-ma-quotes-5\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.598Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.598Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 25}]','jack-ma-quotes-5',28,66),(150,'26',26,'json','[{\"fields\": {\"document\": \"usercontent/user1/maxresdefault.jpg\", \"is_folder\": false, \"title\": \"maxresdefault\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.609Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.609Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 26}]','maxresdefault',28,66),(151,'27',27,'json','[{\"fields\": {\"document\": \"usercontent/user1/jack-ma-quotes.jpg\", \"is_folder\": false, \"title\": \"jack-ma-quotes\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.621Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.621Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 27}]','jack-ma-quotes',28,66),(152,'28',28,'json','[{\"fields\": {\"document\": \"usercontent/user1/BlynQ Logo V1.png\", \"is_folder\": false, \"title\": \"BlynQ Logo V1\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.635Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.635Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/png\"}, \"model\": \"contentManagement.content\", \"pk\": 28}]','BlynQ Logo V1',28,66),(153,'29',29,'json','[{\"fields\": {\"document\": \"usercontent/user1/BlynQ Logo V1 - Blue Background.png\", \"is_folder\": false, \"title\": \"BlynQ Logo V1 - Blue Background\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.646Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.646Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/png\"}, \"model\": \"contentManagement.content\", \"pk\": 29}]','BlynQ Logo V1 - Blue Background',28,66),(154,'30',30,'json','[{\"fields\": {\"document\": \"usercontent/user1/nipun.jpg\", \"is_folder\": false, \"title\": \"nipun\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.664Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.664Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 30}]','nipun',28,66),(155,'31',31,'json','[{\"fields\": {\"document\": \"usercontent/user1/full-stack-python-map.pdf\", \"is_folder\": false, \"title\": \"full-stack-python-map\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:48:11.677Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:48:11.678Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"application/pdf\"}, \"model\": \"contentManagement.content\", \"pk\": 31}]','full-stack-python-map',28,66),(156,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 14146918, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,67),(157,'34',34,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040420.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040420\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.049Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.049Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 34}]','IMG_20160501_040420',28,67),(158,'35',35,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040433.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040433\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.061Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.061Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 35}]','IMG_20160501_040433',28,67),(159,'36',36,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040445.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040445\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.073Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.073Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 36}]','IMG_20160501_040445',28,67),(160,'37',37,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040521.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040521\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.087Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.088Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 37}]','IMG_20160501_040521',28,67),(161,'38',38,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040728.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040728\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.100Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.100Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 38}]','IMG_20160501_040728',28,67),(162,'33',33,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040407.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040407\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.036Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.036Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 33}]','IMG_20160501_040407',28,67),(163,'40',40,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_041930.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_041930\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.123Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.123Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 40}]','IMG_20160501_041930',28,67),(164,'41',41,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_041936.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_041936\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.136Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.136Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 41}]','IMG_20160501_041936',28,67),(165,'42',42,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_041942.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_041942\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.149Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.149Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 42}]','IMG_20160501_041942',28,67),(166,'39',39,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_040800.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_040800\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.111Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.112Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 39}]','IMG_20160501_040800',28,67),(167,'44',44,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_042246.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_042246\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.171Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.171Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 44}]','IMG_20160501_042246',28,67),(168,'43',43,'json','[{\"fields\": {\"document\": \"usercontent/user1/IMG_20160501_042238.jpg\", \"is_folder\": false, \"title\": \"IMG_20160501_042238\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T07:50:14.160Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T07:50:14.160Z\", \"organization\": 1, \"parent_folder\": 16, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 43}]','IMG_20160501_042238',28,67),(169,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 5919156, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,68),(170,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 5929072, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,69),(171,'45',45,'json','[{\"fields\": {\"document\": \"usercontent/user1/Only logo blue_eK9KSi2.png\", \"is_folder\": false, \"title\": \"Only logo blue\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-05T10:23:23.929Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-05T10:23:23.929Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/png\"}, \"model\": \"contentManagement.content\", \"pk\": 45}]','Only logo blue',28,69),(174,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,72),(175,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-06-09T05:54:49.132Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,72),(176,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": null, \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test',26,73),(177,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test device\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": null, \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test device',26,74),(178,'12',12,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:08:50.172Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T14:08:50.165Z\", \"organization\": 1, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 12}]','first',33,75),(179,'12',12,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 12}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 12}]','first-first playlist',32,75),(181,'12',12,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:09:24.415Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T14:08:50.165Z\", \"organization\": 1, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 12}]','first',33,76),(182,'12',12,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 12}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 12}]','first-first playlist',32,76),(187,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,77),(188,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-06-09T14:13:19.720Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,77),(189,'13',13,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:15:15.218Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:15:15.212Z\", \"organization\": 1, \"schedule_title\": \"test 1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 13}]','test 1',33,78),(190,'13',13,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 13}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 13}]','test 1-first playlist',32,78),(192,'17',17,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:23:15.068Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:23:15.059Z\", \"organization\": 1, \"schedule_title\": \"test 12\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 17}]','test 12',33,79),(193,'17',17,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 17}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 17}]','test 12-first playlist',32,79),(194,'19',19,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:24:21.456Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:24:21.440Z\", \"organization\": 1, \"schedule_title\": \"test 13\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 19}]','test 13',33,80),(196,'19',19,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 19}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 19}]','test 13-first playlist',32,80),(197,'20',20,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:25:18.938Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:25:18.929Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 20}]','11',33,81),(199,'20',20,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 20}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 20}]','11-first playlist',32,81),(201,'21',21,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T14:25:55.362Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:25:55.357Z\", \"organization\": 1, \"schedule_title\": \"12\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 21}]','12',33,82),(202,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 21}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','12-first playlist',32,82),(203,'21',21,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:21:29.326Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:25:55.357Z\", \"organization\": 1, \"schedule_title\": \"12\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 21}]','12',33,83),(204,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 21}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','12-first playlist',32,83),(207,'21',21,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:31:49.499Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T14:25:55.357Z\", \"organization\": 1, \"schedule_title\": \"12\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 21}]','12',33,84),(208,'21',21,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 21}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 21}]','12-first playlist',32,84),(209,'22',22,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:32:11.532Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:32:11.517Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 22}]','11',33,85),(210,'22',22,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 22}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 22}]','11-first playlist',32,85),(212,'22',22,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:32:19.201Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:32:11.517Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 22}]','11',33,86),(213,'22',22,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 22}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 22}]','11-first playlist',32,86),(216,'22',22,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:32:39.273Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:32:11.517Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 22}]','11',33,87),(217,'22',22,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 22}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 22}]','11-first playlist',32,87),(220,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:36:49.312Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,88),(221,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,88),(223,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:41:12.242Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,89),(224,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,89),(226,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:41:49.742Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,90),(227,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,90),(229,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T20:42:11.759Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,91),(230,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,91),(233,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-09T21:02:55.481Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,92),(234,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,92),(236,'46',46,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"werwer\", \"url\": \"http://www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-13T10:55:11.827Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-13T10:55:11.827Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 46}]','werwer',28,93),(237,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,94),(238,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-06-13T18:41:51.195Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,94),(239,'47',47,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"google\", \"url\": \"http://www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-13T18:42:16.710Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-13T18:42:16.710Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 47}]','google',28,95),(240,'8',8,'json','[{\"fields\": {\"content\": 47, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 8}]','first playlist - google',29,96),(241,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T06:21:53.376Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,96),(242,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T06:21:53.381Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,96),(243,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,96),(244,'48',48,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abc\", \"url\": \"http://www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T08:00:27.028Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T08:00:27.028Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 48}]','abc',28,97),(245,'49',49,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"defff\", \"url\": \"http://www.blynq.in\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T08:01:31.185Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T08:01:31.185Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 49}]','defff',28,98),(246,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T08:01:41.760Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,99),(247,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T08:01:41.763Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,99),(248,'9',9,'json','[{\"fields\": {\"content\": 49, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 9}]','first playlist - defff',29,99),(249,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,99),(250,'50',50,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abccc\", \"url\": \"http://www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T08:04:11.627Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T08:04:11.627Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 50}]','abccc',28,100),(251,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T08:04:16.248Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,101),(252,'10',10,'json','[{\"fields\": {\"content\": 50, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 10}]','first playlist - abccc',29,101),(253,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T08:04:16.254Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,101),(254,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,101),(255,'51',51,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abc\", \"url\": \"www.abc.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T08:40:49.320Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T08:40:49.320Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 51}]','abc',28,102),(256,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T08:40:56.280Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,103),(257,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T08:40:56.273Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,103),(258,'11',11,'json','[{\"fields\": {\"content\": 51, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 11}]','first playlist - abc',29,103),(259,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,103),(260,'52',52,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"google\", \"url\": \"www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T09:14:02.924Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T09:14:02.924Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 52}]','google',28,104),(261,'53',53,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"google\", \"url\": \"www.google.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T09:14:08.169Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T09:14:08.169Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 53}]','google',28,105),(262,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T09:16:20.321Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,106),(263,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T09:16:20.327Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,106),(264,'12',12,'json','[{\"fields\": {\"content\": 53, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 12}]','first playlist - google',29,106),(265,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,106),(266,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T09:18:21.917Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,107),(267,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T09:18:21.923Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,107),(268,'13',13,'json','[{\"fields\": {\"content\": 52, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 13}]','first playlist - google',29,107),(269,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,107),(270,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T10:23:23.219Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,108),(271,'52',52,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"google\", \"url\": \"www.google.com/\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T09:14:02.924Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:23:11.207Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 52}]','google',28,108),(272,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T10:23:23.239Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,108),(273,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T10:23:43.677Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,109),(274,'52',52,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"google\", \"url\": \"www.google.com/\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T09:14:02.924Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:23:43.633Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": 52}]','google',28,109),(275,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T10:23:43.729Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,109),(276,'-1',-1,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abc\", \"url\": \"abc.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T10:23:56.620Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:23:56.620Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": -1}]','abc',28,110),(277,'-1',-1,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"def\", \"url\": \"def.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T10:23:56.620Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:24:30.022Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": -1}]','def',28,111),(278,'-1',-1,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abc\", \"url\": \"abc.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T10:27:40.715Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:27:40.716Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": -1}]','abc',28,112),(279,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T10:28:56.604Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,113),(280,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T10:28:56.611Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,113),(281,'14',14,'json','[{\"fields\": {\"content\": -1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 14}]','first playlist - abc',29,113),(282,'7',7,'json','[{\"fields\": {\"content\": 11, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 7}]','first playlist - sachin',29,113),(283,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T10:29:12.190Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,114),(284,'-1',-1,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"abc\", \"url\": \"abc.com\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-23T10:27:40.715Z\", \"relative_path\": \"/\", \"content_type\": 3, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-23T10:29:12.181Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"\"}, \"model\": \"contentManagement.content\", \"pk\": -1}]','abc',28,114),(285,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T10:29:12.203Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,114),(286,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-06-23T10:29:19.421Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,115),(287,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-23T10:29:19.439Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,115),(289,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T12:12:11.195Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,116),(290,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,116),(293,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": false, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T12:13:04.235Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,117),(294,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,117),(297,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": false, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T13:51:06.452Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,118),(298,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,118),(301,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T14:22:31.133Z\", \"last_updated_by\": 1, \"is_always\": false, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,119),(302,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,119),(305,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T14:23:29.660Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,120),(306,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,120),(308,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T14:36:26.134Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,121),(309,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,121),(311,'23',23,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-06-27T14:49:03.407Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"organization\": 1, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,122),(312,'23',23,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 23}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 23}]','11-first playlist',32,122),(314,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 6517127, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,123),(315,'12',12,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"francisofassisi121023\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-27T18:11:21.351Z\", \"relative_path\": \"/\", \"content_type\": 8, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-27T18:11:21.375Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/francisofassisi121023.jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 12}]','francisofassisi121023',28,123),(316,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,124),(317,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-06-28T04:51:48.781Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,124),(318,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,125),(319,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-06-28T05:22:46.926Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,125),(320,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 685068415, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,126),(321,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 867001694, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,127),(322,'13',13,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"francisofassisi121023\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-28T08:14:02.183Z\", \"relative_path\": \"/\", \"content_type\": 8, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-28T08:14:02.183Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/francisofassisi121023_BIeKA4y.jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 13}]','francisofassisi121023',28,128),(323,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 866952803, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,129),(324,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 1051704991, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,130),(325,'14',14,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"SREEJAKALYANAM II CHIRANJEEVI DAUGHTER  Wedding Trailer II EPICS BY AVINASH-QL0BsNLG1qY\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-28T08:15:53.137Z\", \"relative_path\": \"/\", \"content_type\": 6, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-28T08:15:53.137Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/SREEJAKALYANAM II CHIRANJEEVI DAUGHTER  Wedding Trailer II EPICS _PGqKlDA.mp4\"}, \"model\": \"contentManagement.content\", \"pk\": 14}]','SREEJAKALYANAM II CHIRANJEEVI DAUGHTER  Wedding Trailer II EPICS BY AVINASH-QL0BsNLG1qY',28,130),(326,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 0, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,131),(327,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 48891, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,132),(328,'15',15,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"francisofassisi121023\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-06-29T13:28:07.459Z\", \"relative_path\": \"/\", \"content_type\": 8, \"uploaded_by\": 1, \"last_modified_time\": \"2016-06-29T13:28:07.459Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/francisofassisi121023.jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 15}]','francisofassisi121023',28,132),(329,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 0, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,133),(330,'16',16,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"charlie chaplin\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-07-02T19:34:36.248Z\", \"relative_path\": \"/\", \"content_type\": 6, \"uploaded_by\": 1, \"last_modified_time\": \"2016-07-02T19:34:36.248Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/charlie chaplin.mp4\"}, \"model\": \"contentManagement.content\", \"pk\": 16}]','charlie chaplin',28,134),(331,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 17475783, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,134),(332,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 0, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,135),(333,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 28856823, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,136),(334,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 57713646, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,137),(335,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 86570469, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,138),(336,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 69094686, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,139),(337,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 51618903, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,140),(338,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34143120, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,141),(339,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 80475726, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,142),(340,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 62999943, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,143),(341,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 45524160, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,144),(342,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 62999943, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,145),(343,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 45524160, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,146),(344,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 62999943, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,147),(345,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 80475726, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,148),(346,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 62999943, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,149),(347,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 45524160, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,150),(348,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 62999943, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,151),(349,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 45524160, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,152),(350,'32',32,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"charlie chaplin\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-07-02T20:28:13.348Z\", \"relative_path\": \"/\", \"content_type\": 6, \"uploaded_by\": 1, \"last_modified_time\": \"2016-07-02T20:28:13.348Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/charlie chaplin_uixXlB8.mp4\"}, \"model\": \"contentManagement.content\", \"pk\": 32}]','charlie chaplin',28,153),(351,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 45524160, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,153),(352,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34143120, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,154),(353,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34143120, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,155),(354,'34',34,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"charlie chaplin\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-07-02T20:30:36.877Z\", \"relative_path\": \"/\", \"content_type\": 6, \"uploaded_by\": 1, \"last_modified_time\": \"2016-07-02T20:30:36.877Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/converted_charlie chaplin.mp4\"}, \"model\": \"contentManagement.content\", \"pk\": 34}]','charlie chaplin',28,155),(355,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34143120, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,156),(356,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34143120, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,157),(357,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 22762080, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,158),(358,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 22762080, \"organization_name\": \"Blynq Pvt Ltd\", \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,159),(359,'38',38,'json','[{\"fields\": {\"is_folder\": false, \"title\": \"charlie chaplin\", \"url\": null, \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-07-05T08:34:08.784Z\", \"relative_path\": \"/\", \"content_type\": 6, \"uploaded_by\": 1, \"last_modified_time\": \"2016-07-05T08:34:08.785Z\", \"organization\": 1, \"parent_folder\": null, \"document\": \"test_usercontent/user1/converted_charlie chaplin.mp4\"}, \"model\": \"contentManagement.content\", \"pk\": 38}]','charlie chaplin',28,159),(360,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,160),(361,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-07-13T06:50:02.865Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,160),(362,'24',24,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T07:36:01.780Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-15T07:36:01.754Z\", \"is_split\": true, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 24}]','first',33,161),(363,'26',26,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T07:44:29.337Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-15T07:44:29.188Z\", \"is_split\": true, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 26}]','first',33,162),(364,'27',27,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 4, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 27}]','first-first playlist',32,162),(365,'26',26,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 3, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 26}]','first-first playlist',32,162),(366,'27',27,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T07:50:06.204Z\", \"created_by\": 1, \"split_screen\": 1, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-15T07:50:06.190Z\", \"is_split\": false, \"schedule_title\": \"abc\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 27}]','abc',33,163),(367,'28',28,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 5, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 28}]','abc-first playlist',32,163),(368,'29',29,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T07:56:39.594Z\", \"created_by\": 1, \"split_screen\": 1, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-15T07:56:39.549Z\", \"is_split\": false, \"schedule_title\": \"abc1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 29}]','abc1',33,164),(369,'29',29,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 6, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 29}]','abc1-first playlist',32,164),(370,'30',30,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T09:43:00.258Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-15T09:43:00.088Z\", \"is_split\": true, \"schedule_title\": \"test 23\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 30}]','test 23',33,165),(371,'30',30,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 7, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 30}]','test 23-first playlist',32,165),(372,'31',31,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 8, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 31}]','test 23-first playlist',32,165),(373,'23',23,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-15T13:00:10.608Z\", \"created_by\": 1, \"split_screen\": 1, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-06-09T20:36:49.288Z\", \"is_split\": false, \"schedule_title\": \"11\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 23}]','11',33,166),(374,'32',32,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 9, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 32}]','first-first playlist',32,167),(375,'33',33,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 10, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 33}]','first-first playlist',32,167),(376,'31',31,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-19T08:27:29.575Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-19T08:27:29.539Z\", \"is_split\": true, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 31}]','first',33,167),(377,'32',32,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 9, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 32}]','first-first playlist',32,168),(378,'33',33,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 10, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 33}]','first-first playlist',32,168),(379,'31',31,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-20T15:27:57.883Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-19T08:27:29.539Z\", \"is_split\": true, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 31}]','first',33,168),(380,'32',32,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 9, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 32}]','first-first playlist',32,169),(381,'33',33,'json','[{\"fields\": {\"playlist\": 1, \"schedule_pane\": 10, \"position_index\": 0}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 33}]','first-first playlist',32,169),(382,'31',31,'json','[{\"fields\": {\"last_updated_time\": \"2016-07-20T16:13:12.559Z\", \"created_by\": 1, \"split_screen\": 2, \"last_updated_by\": 1, \"organization\": 1, \"created_time\": \"2016-07-19T08:27:29.539Z\", \"is_split\": true, \"schedule_title\": \"first\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 31}]','first',33,169),(383,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,170),(384,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-07-28T03:22:40.885Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,170);
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
  `created_by_id` int(11),
  `last_updated_by_id` int(11),
  `organization_id` int(11),
  `is_split` tinyint(1) NOT NULL,
  `layout_id` int(11),
  PRIMARY KEY (`schedule_id`),
  KEY `scheduleManagement_schedule_e93cb7eb` (`created_by_id`),
  KEY `scheduleManagement_schedule_49fa5cc1` (`last_updated_by_id`),
  KEY `scheduleManagement_schedule_26b2345e` (`organization_id`),
  KEY `scheduleManagement_schedule_72bc1be0` (`layout_id`),
  CONSTRAINT `D1e8960ced6145002a4e9f87736e58c2` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `D1f79a50fac92720893bb084428cea7e` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `created_by_id_24b1d5d7e7366f41_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `layout_id_12fbd72aaa0ff037_fk_layoutManagement_layout_layout_id` FOREIGN KEY (`layout_id`) REFERENCES `layoutManagement_layout` (`layout_id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedule`
--

LOCK TABLES `scheduleManagement_schedule` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedule` DISABLE KEYS */;
INSERT INTO `scheduleManagement_schedule` VALUES (31,'first','2016-07-19 08:27:29.539542','2016-07-28 08:16:27.083597',1,1,1,1,2);
/*!40000 ALTER TABLE `scheduleManagement_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_schedulepane`
--

DROP TABLE IF EXISTS `scheduleManagement_schedulepane`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_schedulepane` (
  `schedule_pane_id` int(11) NOT NULL AUTO_INCREMENT,
  `is_always` tinyint(1) NOT NULL,
  `all_day` tinyint(1) NOT NULL,
  `recurrence_absolute` tinyint(1) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `schedule_id` int(11) NOT NULL,
  `layout_pane_id` int(11),
  PRIMARY KEY (`schedule_pane_id`),
  UNIQUE KEY `event_id` (`event_id`),
  KEY `scheduleManagement_schedulepane_9bc70bb9` (`schedule_id`),
  KEY `scheduleManagement_schedulepane_1516ff52` (`layout_pane_id`),
  CONSTRAINT `D480dbfdddffe153a4b79c71cdde2e76` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`),
  CONSTRAINT `D48ba017e3af7141d0711eb8d663b2aa` FOREIGN KEY (`layout_pane_id`) REFERENCES `layoutManagement_layoutpane` (`layout_pane_id`),
  CONSTRAINT `scheduleManagement_event_id_b671dc9aeb7bd20_fk_schedule_event_id` FOREIGN KEY (`event_id`) REFERENCES `schedule_event` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedulepane`
--

LOCK TABLES `scheduleManagement_schedulepane` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedulepane` DISABLE KEYS */;
INSERT INTO `scheduleManagement_schedulepane` VALUES (9,1,1,0,50,31,NULL),(10,0,0,0,51,31,NULL);
/*!40000 ALTER TABLE `scheduleManagement_schedulepane` ENABLE KEYS */;
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
  `schedule_pane_id` int(11),
  PRIMARY KEY (`schedule_playlist_id`),
  KEY `scheduleManagement_scheduleplaylists_5d3a6442` (`playlist_id`),
  KEY `scheduleManagement_scheduleplaylists_865bb759` (`schedule_pane_id`),
  CONSTRAINT `D14cbb3d9d04709e1c3e85ecef80ff83` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`playlist_id`),
  CONSTRAINT `D1fec1b707f7cf7a1ebe96646680cfd1` FOREIGN KEY (`schedule_pane_id`) REFERENCES `scheduleManagement_schedulepane` (`schedule_pane_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_scheduleplaylists`
--

LOCK TABLES `scheduleManagement_scheduleplaylists` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_scheduleplaylists` DISABLE KEYS */;
INSERT INTO `scheduleManagement_scheduleplaylists` VALUES (23,0,1,NULL),(32,0,1,9),(33,0,1,10);
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
  `group_id` int(11) DEFAULT NULL,
  `schedule_id` int(11) NOT NULL,
  `screen_id` int(11),
  PRIMARY KEY (`schedule_screen_id`),
  KEY `sch_group_id_1f92042eee00a477_fk_screenManagement_group_group_id` (`group_id`),
  KEY `scheduleManagement_schedulescreens_9bc70bb9` (`schedule_id`),
  KEY `scheduleManagement_schedulescreens_e4ec8585` (`screen_id`),
  CONSTRAINT `D29edf893c4f7c5fbba5410fe2ce1ccd` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`),
  CONSTRAINT `sch_group_id_1f92042eee00a477_fk_screenManagement_group_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`group_id`),
  CONSTRAINT `screen_id_5aa6103c3cd0e0ad_fk_screenManagement_screen_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`screen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedulescreens`
--

LOCK TABLES `scheduleManagement_schedulescreens` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedulescreens` DISABLE KEYS */;
INSERT INTO `scheduleManagement_schedulescreens` VALUES (9,NULL,31,1),(10,1,31,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_calendar`
--

LOCK TABLES `schedule_calendar` WRITE;
/*!40000 ALTER TABLE `schedule_calendar` DISABLE KEYS */;
INSERT INTO `schedule_calendar` VALUES (1,'jaydev android emulator1',''),(2,'test calendar','test-calendar'),(3,'default','default');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_calendarrelation`
--

LOCK TABLES `schedule_calendarrelation` WRITE;
/*!40000 ALTER TABLE `schedule_calendarrelation` DISABLE KEYS */;
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
  `rule_id` int(11),
  PRIMARY KEY (`id`),
  KEY `schedule_ev_calendar_id_4c9dba94868bbeb0_fk_schedule_calendar_id` (`calendar_id`),
  KEY `schedule_event_creator_id_f3a6304c337da5b_fk_auth_user_id` (`creator_id`),
  KEY `schedule_event_e1150e65` (`rule_id`),
  CONSTRAINT `schedule_ev_calendar_id_4c9dba94868bbeb0_fk_schedule_calendar_id` FOREIGN KEY (`calendar_id`) REFERENCES `schedule_calendar` (`id`),
  CONSTRAINT `schedule_event_creator_id_f3a6304c337da5b_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `schedule_event_rule_id_41a281cbfafd8f64_fk_schedule_rule_id` FOREIGN KEY (`rule_id`) REFERENCES `schedule_rule` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_event`
--

LOCK TABLES `schedule_event` WRITE;
/*!40000 ALTER TABLE `schedule_event` DISABLE KEYS */;
INSERT INTO `schedule_event` VALUES (35,'2016-06-26 18:30:00.000000','2016-06-27 18:29:00.000000','11',NULL,'2016-06-09 20:37:02.108748','2016-07-16 08:31:21.417278',NULL,1,2,37),(36,'2016-06-26 18:30:00.000000','2016-06-27 18:29:00.000000','11',NULL,'2016-06-09 20:37:50.718245','2016-06-09 20:37:50.718542',NULL,2,2,37),(38,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','first',NULL,'2016-07-15 07:42:39.634544','2016-07-15 07:42:39.634589',NULL,3,2,39),(39,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','first',NULL,'2016-07-15 07:42:39.698462','2016-07-15 07:42:39.698511',NULL,3,2,40),(40,'2016-07-15 02:30:00.000000','2016-07-15 12:00:00.000000','first',NULL,'2016-07-15 07:44:29.275903','2016-07-15 07:44:29.276269','2016-07-15 12:00:00.000000',3,2,41),(41,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','first',NULL,'2016-07-15 07:44:29.343507','2016-07-15 07:44:29.343552',NULL,3,2,42),(42,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','abc',NULL,'2016-07-15 07:50:06.228602','2016-07-15 07:50:06.228645',NULL,3,2,43),(43,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','abc1',NULL,'2016-07-15 07:56:39.640312','2016-07-15 07:56:39.640356',NULL,3,2,44),(44,'2016-07-14 18:30:00.000000','2016-07-15 18:29:00.000000','test 23',NULL,'2016-07-15 09:43:00.183767','2016-07-15 09:43:00.183811','2016-07-15 18:29:00.000000',3,2,45),(45,'2016-07-15 02:30:00.000000','2016-07-15 12:00:00.000000','test 23',NULL,'2016-07-15 09:43:00.265280','2016-07-15 09:43:00.265325','2016-07-15 12:00:00.000000',3,2,46),(46,'2016-07-18 18:30:00.000000','2016-07-19 18:29:00.000000','first',NULL,'2016-07-19 08:27:29.563416','2016-07-19 08:27:29.563460',NULL,3,2,47),(47,'2016-07-18 18:30:00.000000','2016-07-19 18:29:00.000000','first',NULL,'2016-07-19 08:27:29.582179','2016-07-19 08:27:29.582221',NULL,3,2,48),(48,'2016-07-19 18:30:00.000000','2016-07-20 18:29:00.000000','first',NULL,'2016-07-20 15:27:57.868323','2016-07-20 15:27:57.868370',NULL,3,2,49),(49,'2016-07-19 18:30:00.000000','2016-07-20 18:29:00.000000','first',NULL,'2016-07-20 15:27:57.891724','2016-07-20 15:27:57.891767',NULL,3,2,50),(50,'2016-07-19 18:30:00.000000','2016-07-20 18:29:00.000000','first',NULL,'2016-07-20 16:13:12.551799','2016-07-20 16:13:12.551824',NULL,3,2,51),(51,'2016-07-20 02:30:00.000000','2016-07-20 12:00:00.000000','first',NULL,'2016-07-20 16:13:12.562941','2016-07-20 16:13:12.562965','2016-07-20 12:00:00.000000',3,2,52);
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
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_rule`
--

LOCK TABLES `schedule_rule` WRITE;
/*!40000 ALTER TABLE `schedule_rule` DISABLE KEYS */;
INSERT INTO `schedule_rule` VALUES (26,'23 2016-06-09 00:00:00.319867+','11','DAILY',NULL),(31,'11','11','DAILY',NULL),(32,'11','11','DAILY','interval:1;;;;'),(33,'11','11','DAILY','interval:1;;;;'),(34,'11','11','DAILY','interval:1;;;;'),(35,'11','11','DAILY','interval:1;;;;'),(36,'11','11','DAILY',NULL),(37,'11','11','DAILY',NULL),(39,'first','first','DAILY',NULL),(40,'first','first','DAILY',NULL),(41,'first','first','DAILY','interval:1;;;;'),(42,'first','first','DAILY',NULL),(43,'abc','abc','DAILY',NULL),(44,'abc1','abc1','DAILY',NULL),(45,'test 23','test 23','DAILY','interval:1;;;;'),(46,'test 23','test 23','DAILY','interval:1;;;;'),(47,'first','first','DAILY',NULL),(48,'first','first','DAILY',NULL),(49,'first','first','DAILY',NULL),(50,'first','first','DAILY',NULL),(51,'first','first','DAILY',NULL),(52,'first','first','DAILY','interval:1;;;;');
/*!40000 ALTER TABLE `schedule_rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_aspectratio`
--

DROP TABLE IF EXISTS `screenManagement_aspectratio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_aspectratio` (
  `aspect_ratio_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `width_component` int(11) NOT NULL,
  `height_component` int(11) NOT NULL,
  `orientation` varchar(20) NOT NULL,
  PRIMARY KEY (`aspect_ratio_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_aspectratio`
--

LOCK TABLES `screenManagement_aspectratio` WRITE;
/*!40000 ALTER TABLE `screenManagement_aspectratio` DISABLE KEYS */;
INSERT INTO `screenManagement_aspectratio` VALUES (1,'4:3 Landscape',4,3,'LANDSCAPE'),(2,'4:3 Portrait',4,3,'PORTRAIT'),(3,'16:9 Landscape',16,9,'LANDSCAPE'),(4,'16:9 Portrait',16,9,'PORTRAIT');
/*!40000 ALTER TABLE `screenManagement_aspectratio` ENABLE KEYS */;
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
  `created_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `last_updated_by_id` int(11),
  `last_updated_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`group_id`),
  KEY `a336d8d83dbde3af1e27c50bab159d86` (`organization_id`),
  KEY `created_by_id_25bf7d25606eb7cf_fk_authentication_userdetails_id` (`created_by_id`),
  KEY `screenManagement_group_49fa5cc1` (`last_updated_by_id`),
  CONSTRAINT `D31222558642e4156c6b8ad79d7820dd` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `a336d8d83dbde3af1e27c50bab159d86` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `created_by_id_25bf7d25606eb7cf_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_group`
--

LOCK TABLES `screenManagement_group` WRITE;
/*!40000 ALTER TABLE `screenManagement_group` DISABLE KEYS */;
INSERT INTO `screenManagement_group` VALUES (1,'Group 1','First group','2016-05-29',1,1,NULL,'2016-06-14 11:14:20.342225');
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
  KEY `created_by_id_389b40aaffecd7bb_fk_authentication_userdetails_id` (`created_by_id`),
  KEY `scr_group_id_25d38b0ae3064275_fk_screenManagement_group_group_id` (`group_id`),
  KEY `screenManagement_groupscreens_e4ec8585` (`screen_id`),
  CONSTRAINT `created_by_id_389b40aaffecd7bb_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `s_screen_id_168b1902c060aef_fk_screenManagement_screen_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`screen_id`),
  CONSTRAINT `scr_group_id_25d38b0ae3064275_fk_screenManagement_group_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_groupscreens`
--

LOCK TABLES `screenManagement_groupscreens` WRITE;
/*!40000 ALTER TABLE `screenManagement_groupscreens` DISABLE KEYS */;
INSERT INTO `screenManagement_groupscreens` VALUES (4,1,1,2),(5,NULL,1,1);
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
  `screen_calendar_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `unique_device_key_id` int(11) NOT NULL,
  `city_id` int(11),
  `last_updated_by_id` int(11),
  `last_updated_time` datetime(6) DEFAULT NULL,
  `last_active_time` datetime(6) NOT NULL,
  PRIMARY KEY (`screen_id`),
  UNIQUE KEY `unique_device_key_id` (`unique_device_key_id`),
  KEY `a7c1ba1e3d46eee1df95a619a8c2f227` (`owned_by_id`),
  KEY `screenManagement_screen_dc91ed4b` (`status_id`),
  KEY `screenManagement_screen_c7141997` (`city_id`),
  KEY `scre_screen_calendar_id_58aceaff89f25de5_fk_schedule_calendar_id` (`screen_calendar_id`),
  KEY `D67d42462e3f1c36ec77e9e9dc09390b` (`activated_by_id`),
  KEY `screenManagement_screen_49fa5cc1` (`last_updated_by_id`),
  CONSTRAINT `D099a9619f8d384185c59ce135083230` FOREIGN KEY (`unique_device_key_id`) REFERENCES `screenManagement_screenactivationkey` (`screen_activation_id`),
  CONSTRAINT `D23b29036e98defa308670106fdeab4f` FOREIGN KEY (`status_id`) REFERENCES `screenManagement_screenstatus` (`screen_status_id`),
  CONSTRAINT `D67d42462e3f1c36ec77e9e9dc09390b` FOREIGN KEY (`activated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `a7c1ba1e3d46eee1df95a619a8c2f227` FOREIGN KEY (`owned_by_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `e9f86220afaf4a2d430a24ba1d36facc` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `scre_screen_calendar_id_58aceaff89f25de5_fk_schedule_calendar_id` FOREIGN KEY (`screen_calendar_id`) REFERENCES `schedule_calendar` (`id`),
  CONSTRAINT `screenMa_city_id_6ada127b1914a468_fk_authentication_city_city_id` FOREIGN KEY (`city_id`) REFERENCES `authentication_city` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screen`
--

LOCK TABLES `screenManagement_screen` WRITE;
/*!40000 ALTER TABLE `screenManagement_screen` DISABLE KEYS */;
INSERT INTO `screenManagement_screen` VALUES (1,'jaydev android emulator',32,'16:9','1190*768','','2016-05-28 13:36:27.202897','PRIVATE',1,1,1,2,1,1,NULL,'2016-06-14 11:14:39.479118','2016-07-28 02:58:08.554363'),(2,'test device',24,NULL,'1024*768','mount fort','2016-05-29 11:47:08.863168','PRIVATE',1,1,2,2,2,1,NULL,'2016-06-14 11:14:39.479118','2016-07-28 02:58:08.554363');
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
  `device_serial_num` varchar(20) DEFAULT NULL,
  `in_use` tinyint(1) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`screen_activation_id`),
  UNIQUE KEY `activation_key` (`activation_key`),
  UNIQUE KEY `device_serial_num` (`device_serial_num`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenactivationkey`
--

LOCK TABLES `screenManagement_screenactivationkey` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenactivationkey` DISABLE KEYS */;
INSERT INTO `screenManagement_screenactivationkey` VALUES (1,'a197cb391f0698e5','android emulator jay',1,1),(2,'1234567890','abc def',0,0);
/*!40000 ALTER TABLE `screenManagement_screenactivationkey` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenstatus`
--

LOCK TABLES `screenManagement_screenstatus` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenstatus` DISABLE KEYS */;
INSERT INTO `screenManagement_screenstatus` VALUES (1,'Online','The screen is on and connected to the internet'),(2,'Offline','The screen is either offline or not connected to the internet');
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

-- Dump completed on 2016-07-28 15:45:22
