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
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add calendar',7,'add_calendar'),(20,'Can change calendar',7,'change_calendar'),(21,'Can delete calendar',7,'delete_calendar'),(22,'Can add calendar relation',8,'add_calendarrelation'),(23,'Can change calendar relation',8,'change_calendarrelation'),(24,'Can delete calendar relation',8,'delete_calendarrelation'),(25,'Can add rule',9,'add_rule'),(26,'Can change rule',9,'change_rule'),(27,'Can delete rule',9,'delete_rule'),(28,'Can add event',10,'add_event'),(29,'Can change event',10,'change_event'),(30,'Can delete event',10,'delete_event'),(31,'Can add event relation',11,'add_eventrelation'),(32,'Can change event relation',11,'change_eventrelation'),(33,'Can delete event relation',11,'delete_eventrelation'),(34,'Can add occurrence',12,'add_occurrence'),(35,'Can change occurrence',12,'change_occurrence'),(36,'Can delete occurrence',12,'delete_occurrence'),(37,'Can add revision',13,'add_revision'),(38,'Can change revision',13,'change_revision'),(39,'Can delete revision',13,'delete_revision'),(40,'Can add version',14,'add_version'),(41,'Can change version',14,'change_version'),(42,'Can delete version',14,'delete_version'),(43,'Can add city',15,'add_city'),(44,'Can change city',15,'change_city'),(45,'Can delete city',15,'delete_city'),(46,'Can add address',16,'add_address'),(47,'Can change address',16,'change_address'),(48,'Can delete address',16,'delete_address'),(49,'Can add organization',17,'add_organization'),(50,'Can change organization',17,'change_organization'),(51,'Can delete organization',17,'delete_organization'),(52,'Can add role',18,'add_role'),(53,'Can change role',18,'change_role'),(54,'Can delete role',18,'delete_role'),(55,'Can add user details',19,'add_userdetails'),(56,'Can change user details',19,'change_userdetails'),(57,'Can delete user details',19,'delete_userdetails'),(58,'Can add requested quote',20,'add_requestedquote'),(59,'Can change requested quote',20,'change_requestedquote'),(60,'Can delete requested quote',20,'delete_requestedquote'),(61,'Can add screen status',21,'add_screenstatus'),(62,'Can change screen status',21,'change_screenstatus'),(63,'Can delete screen status',21,'delete_screenstatus'),(64,'Can add screen specs',22,'add_screenspecs'),(65,'Can change screen specs',22,'change_screenspecs'),(66,'Can delete screen specs',22,'delete_screenspecs'),(67,'Can add screen activation key',23,'add_screenactivationkey'),(68,'Can change screen activation key',23,'change_screenactivationkey'),(69,'Can delete screen activation key',23,'delete_screenactivationkey'),(70,'Can add group',24,'add_group'),(71,'Can change group',24,'change_group'),(72,'Can delete group',24,'delete_group'),(73,'Can add group screens',25,'add_groupscreens'),(74,'Can change group screens',25,'change_groupscreens'),(75,'Can delete group screens',25,'delete_groupscreens'),(76,'Can add screen',26,'add_screen'),(77,'Can change screen',26,'change_screen'),(78,'Can delete screen',26,'delete_screen'),(79,'Can add content type',27,'add_contenttype'),(80,'Can change content type',27,'change_contenttype'),(81,'Can delete content type',27,'delete_contenttype'),(82,'Can add content',28,'add_content'),(83,'Can change content',28,'change_content'),(84,'Can delete content',28,'delete_content'),(85,'Can add playlist items',29,'add_playlistitems'),(86,'Can change playlist items',29,'change_playlistitems'),(87,'Can delete playlist items',29,'delete_playlistitems'),(88,'Can add playlist',30,'add_playlist'),(89,'Can change playlist',30,'change_playlist'),(90,'Can delete playlist',30,'delete_playlist'),(91,'Can add schedule screens',31,'add_schedulescreens'),(92,'Can change schedule screens',31,'change_schedulescreens'),(93,'Can delete schedule screens',31,'delete_schedulescreens'),(94,'Can add schedule playlists',32,'add_scheduleplaylists'),(95,'Can change schedule playlists',32,'change_scheduleplaylists'),(96,'Can delete schedule playlists',32,'delete_scheduleplaylists'),(97,'Can add schedule',33,'add_schedule'),(98,'Can change schedule',33,'change_schedule'),(99,'Can delete schedule',33,'delete_schedule');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=','2016-05-28 13:20:05.178153',1,'admin','','','hello@blynq.in',1,1,'2016-05-27 10:29:30.217333'),(2,'pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=','2016-05-28 13:16:23.455576',1,'nipun','Nipun','Edara','nipun425@gmail.com',1,1,'2016-05-27 10:32:28.000000');
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
  `added_by_id` int(11),
  `city_id` int(11) NOT NULL,
  PRIMARY KEY (`address_id`),
  UNIQUE KEY `authentication_address_building_name_307a710555774b15_uniq` (`building_name`,`added_by_id`),
  KEY `authentication_address_0c5d7d4e` (`added_by_id`),
  KEY `authentication_address_c7141997` (`city_id`),
  CONSTRAINT `au_added_by_id_3583ba7a32ee1cf1_fk_authentication_userdetails_id` FOREIGN KEY (`added_by_id`) REFERENCES `authentication_userdetails` (`id`),
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
  `city_name` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `name` (`city_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_city`
--

LOCK TABLES `authentication_city` WRITE;
/*!40000 ALTER TABLE `authentication_city` DISABLE KEYS */;
INSERT INTO `authentication_city` VALUES (1,'Hyderabad','Telangana'),(2,'Visakhapatnam','Andhra Pradesh');
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
  `address` varchar(100) DEFAULT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `total_file_size_limit` bigint(20) NOT NULL,
  `used_file_size` bigint(20) NOT NULL,
  PRIMARY KEY (`organization_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_organization`
--

LOCK TABLES `authentication_organization` WRITE;
/*!40000 ALTER TABLE `authentication_organization` DISABLE KEYS */;
INSERT INTO `authentication_organization` VALUES (1,'Blynq Pvt Ltd','http://www.blynq.in','G1, Mount Fort, Pragathi Nagar, Hyderabad','8277121319',1073741824,594759);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_role`
--

LOCK TABLES `authentication_role` WRITE;
/*!40000 ALTER TABLE `authentication_role` DISABLE KEYS */;
INSERT INTO `authentication_role` VALUES (1,'manager','Has read/edit access to all the company information');
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
  `original_filename` varchar(100) DEFAULT NULL,
  `document_type` varchar(50) DEFAULT NULL,
  `uploaded_time` datetime(6) NOT NULL,
  `last_modified_time` datetime(6) NOT NULL,
  `is_folder` tinyint(1) NOT NULL,
  `relative_path` varchar(1025) NOT NULL,
  `last_modified_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  `parent_folder_id` int(11) DEFAULT NULL,
  `uploaded_by_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`content_id`),
  KEY `D5bd4182a66a7dc9e4dbc49d79b84d24` (`last_modified_by_id`),
  KEY `D030273c9e61c272ad95472f688031ac` (`organization_id`),
  KEY `c28200b62fd5064ce5f884826faee3c7` (`parent_folder_id`),
  KEY `D9406e8f168fd432bee791784e0f2ca1` (`uploaded_by_id`),
  CONSTRAINT `D030273c9e61c272ad95472f688031ac` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `D5bd4182a66a7dc9e4dbc49d79b84d24` FOREIGN KEY (`last_modified_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `D9406e8f168fd432bee791784e0f2ca1` FOREIGN KEY (`uploaded_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `c28200b62fd5064ce5f884826faee3c7` FOREIGN KEY (`parent_folder_id`) REFERENCES `contentManagement_content` (`content_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_content`
--

LOCK TABLES `contentManagement_content` WRITE;
/*!40000 ALTER TABLE `contentManagement_content` DISABLE KEYS */;
INSERT INTO `contentManagement_content` VALUES (2,'temp folder','','',NULL,'folder','2016-05-29 12:38:25.475193','2016-05-29 18:46:29.461550',1,'/',1,1,NULL,1),(3,'sachin','usercontent/1/sachin.jpg','',NULL,'image/jpeg','2016-05-29 13:12:22.456208','2016-05-31 04:39:50.341316',0,'/',1,1,2,1),(4,'account_statement','usercontent/1/account_statement.pdf','',NULL,'application/pdf','2016-05-31 04:37:34.376997','2016-05-31 04:39:13.700106',0,'/',1,1,2,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-05-27 10:31:25.847971','1','Blynq Pvt Ltd',1,'',17,1),(2,'2016-05-27 10:32:22.970936','1','manager',1,'',18,1),(3,'2016-05-27 10:32:28.288885','2','nipun',1,'',4,1),(4,'2016-05-27 10:33:07.503182','2','nipun',2,'Changed first_name, last_name, email, is_staff, is_superuser and last_login. Changed mobile_number for user details \"nipun\".',4,1),(5,'2016-05-28 13:20:32.220445','1','serial number android emulator jay key a197cb391f0698e5',1,'',23,1),(6,'2016-05-28 13:23:46.603616','1','Online',1,'',21,1),(7,'2016-05-28 13:34:14.115958','2','Offline',1,'',21,1),(8,'2016-05-29 10:35:23.672811','1','Hyderabad, Telangana',1,'',15,1),(9,'2016-05-29 10:35:54.757843','2','Visakhapatnam, Andhra Pradesh',1,'',15,1),(10,'2016-05-29 10:36:32.719708','1','jaydev android emulator',2,'Changed city.',26,1),(11,'2016-05-29 11:04:13.293057','1','Group 1',1,'',24,1),(12,'2016-05-29 11:04:55.817976','1','jaydev android emulator-Group 1',1,'',25,1),(13,'2016-05-29 11:41:35.631796','2','Group 2',1,'',24,1),(14,'2016-05-29 11:45:24.717899','2','serial number abc def key 1234567890',1,'',23,1),(15,'2016-05-29 11:47:05.962391','2','test calendar',1,'',7,1),(16,'2016-05-29 11:47:08.864510','2','test',1,'',26,1),(17,'2016-05-29 14:31:29.948299','2','First schedule',1,'',33,1),(18,'2016-05-29 14:31:38.563753','1','first schedule',3,'',33,1),(19,'2016-05-29 14:32:34.758236','1','first event: May 29, 2016 - May 29, 2016',1,'',10,1),(20,'2016-05-29 14:32:37.606405','1','First schedule - screen jaydev android emulator',1,'',31,1),(21,'2016-05-29 14:32:50.123950','2','First schedule-first playlist',1,'',32,1),(22,'2016-05-29 14:52:26.187749','1','First schedule - screen jaydev android emulator - group Group 1',2,'Changed group.',31,1),(23,'2016-05-29 14:59:55.860252','2','test: May 29, 2016 - May 29, 2016',1,'',10,1),(24,'2016-05-29 14:59:57.867887','2','First schedule - screen jaydev android emulator',1,'',31,1),(25,'2016-05-29 20:11:31.452390','3','temp1',3,'',33,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(16,'authentication','address'),(15,'authentication','city'),(17,'authentication','organization'),(20,'authentication','requestedquote'),(18,'authentication','role'),(19,'authentication','userdetails'),(28,'contentManagement','content'),(27,'contentManagement','contenttype'),(5,'contenttypes','contenttype'),(30,'playlistManagement','playlist'),(29,'playlistManagement','playlistitems'),(13,'reversion','revision'),(14,'reversion','version'),(7,'schedule','calendar'),(8,'schedule','calendarrelation'),(10,'schedule','event'),(11,'schedule','eventrelation'),(12,'schedule','occurrence'),(9,'schedule','rule'),(33,'scheduleManagement','schedule'),(32,'scheduleManagement','scheduleplaylists'),(31,'scheduleManagement','schedulescreens'),(24,'screenManagement','group'),(25,'screenManagement','groupscreens'),(26,'screenManagement','screen'),(23,'screenManagement','screenactivationkey'),(22,'screenManagement','screenspecs'),(21,'screenManagement','screenstatus'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-05-27 10:26:10.049497'),(2,'auth','0001_initial','2016-05-27 10:26:10.689228'),(3,'admin','0001_initial','2016-05-27 10:26:10.844101'),(4,'contenttypes','0002_remove_content_type_name','2016-05-27 10:26:10.973854'),(5,'auth','0002_alter_permission_name_max_length','2016-05-27 10:26:11.043031'),(6,'auth','0003_alter_user_email_max_length','2016-05-27 10:26:11.103787'),(7,'auth','0004_alter_user_username_opts','2016-05-27 10:26:11.124732'),(8,'auth','0005_alter_user_last_login_null','2016-05-27 10:26:11.186766'),(9,'auth','0006_require_contenttypes_0002','2016-05-27 10:26:11.191124'),(10,'authentication','0001_initial','2016-05-27 10:26:11.936689'),(11,'contentManagement','0001_initial','2016-05-27 10:26:12.222907'),(12,'playlistManagement','0001_initial','2016-05-27 10:26:12.635050'),(13,'reversion','0001_initial','2016-05-27 10:26:12.974337'),(14,'reversion','0002_auto_20141216_1509','2016-05-27 10:26:13.084752'),(15,'schedule','0001_initial','2016-05-27 10:26:13.958068'),(16,'screenManagement','0001_initial','2016-05-27 10:26:15.357763'),(17,'scheduleManagement','0001_initial','2016-05-27 10:26:15.560291'),(18,'scheduleManagement','0002_auto_20160527_1025','2016-05-27 10:26:17.312932'),(19,'sessions','0001_initial','2016-05-27 10:26:17.381577'),(20,'screenManagement','0002_auto_20160528_1336','2016-05-28 13:36:20.494814'),(21,'screenManagement','0003_auto_20160529_0716','2016-05-29 07:17:14.980089'),(22,'screenManagement','0004_screen_city','2016-05-29 07:42:54.651276'),(23,'authentication','0002_auto_20160529_1050','2016-05-29 10:50:15.868640'),(24,'contentManagement','0002_auto_20160531_0559','2016-05-31 05:59:12.510681');
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
INSERT INTO `django_session` VALUES ('il3vfcgn1n1dgmlznpw88qmagpurasyt','MDU1MzdmYjBmZjBmNzliNTMyNDAwODIxMDM4ZTcxOWIxMjZjYmM3Njp7Il9hdXRoX3VzZXJfaGFzaCI6IjZlNDViNGNiNTMzMjYzMzEzMjdkMGE2ZDE3ZjZlMWFiN2I0NzUyNWMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyIn0=','2016-06-11 13:16:23.463886');
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
  `playlist_total_time` int(11) DEFAULT NULL,
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
INSERT INTO `playlistManagement_playlist` VALUES (1,'first playlist',30,'2016-05-29 13:06:52.524586','2016-05-29 13:55:01.408389',1,1,1);
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
INSERT INTO `playlistManagement_playlistitems` VALUES (5,0,15,3,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_revision`
--

LOCK TABLES `reversion_revision` WRITE;
/*!40000 ALTER TABLE `reversion_revision` DISABLE KEYS */;
INSERT INTO `reversion_revision` VALUES (1,'default','2016-05-27 10:29:38.108787','',1),(2,'default','2016-05-27 10:31:25.863484','Initial version.',1),(3,'default','2016-05-27 10:32:28.318508','Initial version.',1),(4,'default','2016-05-27 10:33:07.521794','Changed first_name, last_name, email, is_staff, is_superuser and last_login. Changed mobile_number for user details \"nipun\".',1),(5,'default','2016-05-27 10:33:37.728837','',2),(6,'default','2016-05-28 13:16:23.718135','',2),(7,'default','2016-05-28 13:20:05.299312','',1),(8,'default','2016-05-28 13:36:27.266907','',2),(9,'default','2016-05-29 10:36:32.905106','Changed city.',1),(10,'default','2016-05-29 11:04:13.463652','Initial version.',1),(11,'default','2016-05-29 11:04:55.823768','Initial version.',1),(12,'default','2016-05-29 11:41:35.813753','Initial version.',1),(13,'default','2016-05-29 11:47:09.042238','Initial version.',1),(14,'default','2016-05-29 12:38:15.688195','',2),(15,'default','2016-05-29 12:38:25.479914','',2),(16,'default','2016-05-29 13:06:52.795248','',2),(17,'default','2016-05-29 13:07:01.476722','',2),(18,'default','2016-05-29 13:07:06.481637','',2),(19,'default','2016-05-29 13:12:22.464073','',2),(20,'default','2016-05-29 13:12:35.492765','',2),(21,'default','2016-05-29 13:54:29.440872','',2),(22,'default','2016-05-29 13:55:01.442131','',2),(23,'default','2016-05-29 14:17:25.437525','',2),(24,'default','2016-05-29 14:31:29.956282','Initial version.',1),(25,'default','2016-05-29 14:32:37.614493','Initial version.',1),(26,'default','2016-05-29 14:32:50.128573','Initial version.',1),(27,'default','2016-05-29 14:52:26.344940','Changed group.',1),(28,'default','2016-05-29 14:59:58.040854','Initial version.',1),(29,'default','2016-05-29 20:11:20.178482','',2),(30,'default','2016-05-30 18:58:38.678561','',2),(31,'default','2016-05-30 20:10:36.184391','',2),(32,'default','2016-05-30 20:13:18.837271','',2),(33,'default','2016-05-30 20:14:16.641664','',2),(34,'default','2016-05-30 20:15:02.785046','',2),(35,'default','2016-05-30 20:37:09.502075','',2),(36,'default','2016-05-30 21:15:33.534795','',2),(37,'default','2016-05-31 04:37:34.395124','',2),(38,'default','2016-05-31 04:39:13.705697','',2),(39,'default','2016-05-31 04:39:50.347624','',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reversion_version`
--

LOCK TABLES `reversion_version` WRITE;
/*!40000 ALTER TABLE `reversion_version` DISABLE KEYS */;
INSERT INTO `reversion_version` VALUES (1,'1',1,'json','[{\"fields\": {\"username\": \"admin\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:29:37.895Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=\", \"email\": \"hello@blynq.in\", \"date_joined\": \"2016-05-27T10:29:30.217Z\"}, \"model\": \"auth.user\", \"pk\": 1}]','admin',4,1),(2,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 0, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,2),(3,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"8277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,3),(4,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": false, \"is_staff\": false, \"last_login\": null, \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"\", \"date_joined\": \"2016-05-27T10:32:28.226Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,3),(5,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,4),(6,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:33:02Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,4),(7,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,5),(8,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-27T10:33:37.691Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,5),(9,'1',1,'json','[{\"fields\": {\"organization\": 1, \"role\": 1, \"user\": 2, \"mobile_number\": \"918277121319\"}, \"model\": \"authentication.userdetails\", \"pk\": 1}]','nipun',19,6),(10,'2',2,'json','[{\"fields\": {\"username\": \"nipun\", \"first_name\": \"Nipun\", \"last_name\": \"Edara\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-28T13:16:23.455Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$1fD2IEv28Hwg$Ckx5FHpwxe40g4bTiD9Hq9M49lK0tGMVb6GcgXlTiHM=\", \"email\": \"nipun425@gmail.com\", \"date_joined\": \"2016-05-27T10:32:28Z\"}, \"model\": \"auth.user\", \"pk\": 2}]','nipun',4,6),(11,'1',1,'json','[{\"fields\": {\"username\": \"admin\", \"first_name\": \"\", \"last_name\": \"\", \"is_active\": true, \"is_superuser\": true, \"is_staff\": true, \"last_login\": \"2016-05-28T13:20:05.178Z\", \"groups\": [], \"user_permissions\": [], \"password\": \"pbkdf2_sha256$20000$XH4uzmLIkawj$jrS7ZWWl+RtJoIZV22urw7xr/RaktQikVA7J4Tq+Pxo=\", \"email\": \"hello@blynq.in\", \"date_joined\": \"2016-05-27T10:29:30.217Z\"}, \"model\": \"auth.user\", \"pk\": 1}]','admin',4,7),(12,'1',1,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"status\": 2, \"activated_by\": 1, \"screen_name\": \"jaydev android emulator\", \"screen_calendar\": 1, \"screen_size\": 32, \"address\": \"\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 1, \"resolution\": \"1190*768\", \"activated_on\": \"2016-05-28T13:36:27.202Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 1}]','jaydev android emulator',26,8),(13,'1',1,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"jaydev android emulator\", \"screen_calendar\": 1, \"screen_size\": 32, \"status\": 2, \"address\": \"\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 1, \"resolution\": \"1190*768\", \"activated_on\": \"2016-05-28T13:36:27.202Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 1}]','jaydev android emulator',26,9),(14,'1',1,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-29\", \"description\": \"First group\", \"created_by\": 1, \"group_name\": \"Group 1\"}, \"model\": \"screenManagement.group\", \"pk\": 1}]','Group 1',24,10),(15,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": 1, \"created_by\": 1}, \"model\": \"screenManagement.groupscreens\", \"pk\": 1}]','jaydev android emulator-Group 1',25,11),(16,'2',2,'json','[{\"fields\": {\"organization\": 1, \"created_on\": \"2016-05-29\", \"description\": \"The second group\", \"created_by\": 1, \"group_name\": \"Group 2\"}, \"model\": \"screenManagement.group\", \"pk\": 2}]','Group 2',24,12),(17,'2',2,'json','[{\"fields\": {\"business_type\": \"PRIVATE\", \"city\": 1, \"activated_by\": 1, \"screen_name\": \"test\", \"screen_calendar\": 2, \"screen_size\": 24, \"status\": 2, \"address\": \"mount fort\", \"aspect_ratio\": \"16:9\", \"owned_by\": 1, \"unique_device_key\": 2, \"resolution\": \"1024*768\", \"activated_on\": \"2016-05-29T11:47:08.863Z\"}, \"model\": \"screenManagement.screen\", \"pk\": 2}]','test',26,13),(18,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 34373, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,14),(19,'1',1,'json','[{\"fields\": {\"document\": \"usercontent/1/fuck_you_bitches.jpg\", \"is_folder\": false, \"title\": \"fuck_you_bitches\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T12:38:15.549Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T12:38:15.550Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 1}]','fuck_you_bitches',28,14),(20,'2',2,'json','[{\"fields\": {\"document\": \"\", \"is_folder\": true, \"title\": \"temp folder\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T12:38:25.475Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T12:38:25.475Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpg\"}, \"model\": \"contentManagement.content\", \"pk\": 2}]','temp folder',28,15),(21,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 0, \"last_updated_time\": \"2016-05-29T13:06:52.533Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,16),(22,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 15, \"last_updated_time\": \"2016-05-29T13:07:01.464Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,17),(23,'1',1,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 1}]','first playlist - fuck_you_bitches',29,17),(24,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:07:06.460Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,18),(25,'2',2,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 2}]','first playlist - fuck_you_bitches',29,18),(26,'1',1,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 1}]','first playlist - fuck_you_bitches',29,18),(27,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 308913, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,19),(28,'3',3,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T13:12:22.456Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-29T13:12:22.456Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 3}]','sachin',28,19),(29,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:12:35.462Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,20),(30,'3',3,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 3}]','first playlist - sachin',29,20),(31,'4',4,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 4}]','first playlist - sachin',29,20),(32,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 60, \"last_updated_time\": \"2016-05-29T13:54:29.187Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,21),(33,'3',3,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 3}]','first playlist - sachin',29,21),(34,'4',4,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 4}]','first playlist - sachin',29,21),(35,'5',5,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 2}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 5}]','first playlist - sachin',29,21),(36,'6',6,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 3}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 6}]','first playlist - fuck_you_bitches',29,21),(37,'1',1,'json','[{\"fields\": {\"playlist_total_time\": 30, \"last_updated_time\": \"2016-05-29T13:55:01.408Z\", \"created_by\": 1, \"last_updated_by\": 1, \"created_time\": \"2016-05-29T13:06:52.524Z\", \"organization\": 1, \"playlist_title\": \"first playlist\"}, \"model\": \"playlistManagement.playlist\", \"pk\": 1}]','first playlist',30,22),(38,'5',5,'json','[{\"fields\": {\"content\": 3, \"playlist\": 1, \"display_time\": 15, \"position_index\": 0}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 5}]','first playlist - sachin',29,22),(39,'6',6,'json','[{\"fields\": {\"content\": 1, \"playlist\": 1, \"display_time\": 15, \"position_index\": 1}, \"model\": \"playlistManagement.playlistitems\", \"pk\": 6}]','first playlist - fuck_you_bitches',29,22),(40,'1',1,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T14:17:25.174Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:17:25.147Z\", \"organization\": 1, \"schedule_title\": \"first schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 1}]','first schedule',33,23),(41,'1',1,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 1}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 1}]','first schedule-first playlist',32,23),(42,'2',2,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T14:31:29.947Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:31:29.947Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 2}]','First schedule',33,24),(43,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 1, \"schedule\": 2}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen jaydev android emulator',31,25),(44,'2',2,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 1, \"schedule\": 2}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-first playlist',32,26),(45,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": 1, \"event\": 1, \"schedule\": 2}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen jaydev android emulator - group Group 1',31,27),(46,'2',2,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 2, \"schedule\": 2}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 2}]','First schedule - screen jaydev android emulator',31,28),(47,'3',3,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-29T20:11:20.010Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T20:11:19.996Z\", \"organization\": 1, \"schedule_title\": \"temp1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 3}]','temp1',33,29),(48,'3',3,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 3}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 3}]','temp1-first playlist',32,29),(49,'4',4,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T18:58:38.471Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T18:58:38.426Z\", \"organization\": 1, \"schedule_title\": \"1\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 4}]','1',33,30),(50,'3',3,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 3, \"schedule\": 4}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 3}]','1 - screen jaydev android emulator',31,30),(51,'4',4,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 4}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 4}]','1-first playlist',32,30),(52,'4',4,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 4, \"schedule\": 5}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 4}]','2 - screen jaydev android emulator',31,31),(53,'5',5,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:10:35.985Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:10:35.973Z\", \"organization\": 1, \"schedule_title\": \"2\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 5}]','2',33,31),(54,'5',5,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 5}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 5}]','2-first playlist',32,31),(55,'6',6,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:13:18.641Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:13:18.631Z\", \"organization\": 1, \"schedule_title\": \"3\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 6}]','3',33,32),(56,'6',6,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 6}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 6}]','3-first playlist',32,32),(57,'7',7,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:14:16.627Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:14:16.615Z\", \"organization\": 1, \"schedule_title\": \"3\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 7}]','3',33,33),(58,'7',7,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 7}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 7}]','3-first playlist',32,33),(59,'8',8,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:15:02.593Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:15:02.583Z\", \"organization\": 1, \"schedule_title\": \"4\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 8}]','4',33,34),(60,'8',8,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 8}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 8}]','4-first playlist',32,34),(61,'9',9,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T20:37:09.278Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-30T20:37:09.262Z\", \"organization\": 1, \"schedule_title\": \"4\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 9}]','4',33,35),(62,'5',5,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 5, \"schedule\": 9}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 5}]','4 - screen jaydev android emulator',31,35),(63,'9',9,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 9}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 9}]','4-first playlist',32,35),(64,'1',1,'json','[{\"fields\": {\"screen\": 1, \"group\": 1, \"event\": 6, \"schedule\": 2}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 1}]','First schedule - screen jaydev android emulator - group Group 1',31,36),(65,'2',2,'json','[{\"fields\": {\"recurrence_absolute\": false, \"all_day\": true, \"created_by\": 1, \"last_updated_time\": \"2016-05-30T21:15:33.230Z\", \"last_updated_by\": 1, \"is_always\": true, \"created_time\": \"2016-05-29T14:31:29.947Z\", \"organization\": 1, \"schedule_title\": \"First schedule\"}, \"model\": \"scheduleManagement.schedule\", \"pk\": 2}]','First schedule',33,36),(66,'2',2,'json','[{\"fields\": {\"playlist\": 1, \"position_index\": 0, \"schedule\": 2}, \"model\": \"scheduleManagement.scheduleplaylists\", \"pk\": 2}]','First schedule-first playlist',32,36),(67,'2',2,'json','[{\"fields\": {\"screen\": 1, \"group\": null, \"event\": 2, \"schedule\": 2}, \"model\": \"scheduleManagement.schedulescreens\", \"pk\": 2}]','First schedule - screen jaydev android emulator',31,36),(68,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 314566, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,37),(69,'4',4,'json','[{\"fields\": {\"document\": \"usercontent/1/account_statement.pdf\", \"is_folder\": false, \"title\": \"account_statement\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T04:37:34.376Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:37:34.377Z\", \"organization\": 1, \"parent_folder\": null, \"document_type\": \"application/pdf\"}, \"model\": \"contentManagement.content\", \"pk\": 4}]','account_statement',28,37),(70,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 320219, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,38),(71,'4',4,'json','[{\"fields\": {\"document\": \"usercontent/1/account_statement.pdf\", \"is_folder\": false, \"title\": \"account_statement\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-31T04:37:34.376Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:39:13.700Z\", \"organization\": 1, \"parent_folder\": 2, \"document_type\": \"application/pdf\"}, \"model\": \"contentManagement.content\", \"pk\": 4}]','account_statement',28,38),(72,'1',1,'json','[{\"fields\": {\"website\": \"http://www.blynq.in\", \"name\": \"Blynq Pvt Ltd\", \"total_file_size_limit\": 1073741824, \"used_file_size\": 594759, \"contact\": \"8277121319\", \"address\": \"G1, Mount Fort, Pragathi Nagar, Hyderabad\"}, \"model\": \"authentication.organization\", \"pk\": 1}]','Blynq Pvt Ltd',17,39),(73,'3',3,'json','[{\"fields\": {\"document\": \"usercontent/1/sachin.jpg\", \"is_folder\": false, \"title\": \"sachin\", \"last_modified_by\": 1, \"sha1_hash\": \"\", \"uploaded_time\": \"2016-05-29T13:12:22.456Z\", \"relative_path\": \"/\", \"original_filename\": null, \"uploaded_by\": 1, \"last_modified_time\": \"2016-05-31T04:39:50.341Z\", \"organization\": 1, \"parent_folder\": 2, \"document_type\": \"image/jpeg\"}, \"model\": \"contentManagement.content\", \"pk\": 3}]','sachin',28,39);
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
  `is_always` tinyint(1) NOT NULL,
  `all_day` tinyint(1) NOT NULL,
  `recurrence_absolute` tinyint(1) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11),
  `last_updated_by_id` int(11),
  `organization_id` int(11),
  PRIMARY KEY (`schedule_id`),
  KEY `scheduleManagement_schedule_e93cb7eb` (`created_by_id`),
  KEY `scheduleManagement_schedule_49fa5cc1` (`last_updated_by_id`),
  KEY `scheduleManagement_schedule_26b2345e` (`organization_id`),
  CONSTRAINT `D1e8960ced6145002a4e9f87736e58c2` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `D1f79a50fac92720893bb084428cea7e` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `created_by_id_24b1d5d7e7366f41_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedule`
--

LOCK TABLES `scheduleManagement_schedule` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedule` DISABLE KEYS */;
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
  `schedule_id` int(11),
  PRIMARY KEY (`schedule_playlist_id`),
  KEY `scheduleManagement_scheduleplaylists_5d3a6442` (`playlist_id`),
  KEY `scheduleManagement_scheduleplaylists_9bc70bb9` (`schedule_id`),
  CONSTRAINT `D14cbb3d9d04709e1c3e85ecef80ff83` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`playlist_id`),
  CONSTRAINT `fae4cee4482027edf411bf20126c431d` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_scheduleplaylists`
--

LOCK TABLES `scheduleManagement_scheduleplaylists` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_scheduleplaylists` DISABLE KEYS */;
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
  `group_id` int(11),
  `schedule_id` int(11) NOT NULL,
  `screen_id` int(11),
  PRIMARY KEY (`schedule_screen_id`),
  UNIQUE KEY `event_id` (`event_id`),
  KEY `scheduleManagement_schedulescreens_0e939a4f` (`group_id`),
  KEY `scheduleManagement_schedulescreens_9bc70bb9` (`schedule_id`),
  KEY `scheduleManagement_schedulescreens_e4ec8585` (`screen_id`),
  CONSTRAINT `D29edf893c4f7c5fbba5410fe2ce1ccd` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`schedule_id`),
  CONSTRAINT `sch_group_id_1f92042eee00a477_fk_screenManagement_group_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`group_id`),
  CONSTRAINT `scheduleManagemen_event_id_151cbcd7ab0f3afc_fk_schedule_event_id` FOREIGN KEY (`event_id`) REFERENCES `schedule_event` (`id`),
  CONSTRAINT `screen_id_5aa6103c3cd0e0ad_fk_screenManagement_screen_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`screen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedulescreens`
--

LOCK TABLES `scheduleManagement_schedulescreens` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedulescreens` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_event`
--

LOCK TABLES `schedule_event` WRITE;
/*!40000 ALTER TABLE `schedule_event` DISABLE KEYS */;
INSERT INTO `schedule_event` VALUES (2,'2016-05-30 00:00:00.231182','2016-05-30 23:59:59.231195','First schedule','test','2016-05-29 14:59:55.859024','2016-05-30 21:15:33.243388',NULL,2,2,9),(3,'2016-05-30 00:00:00.482900','2016-05-30 23:59:59.482922','1',NULL,'2016-05-30 18:58:38.504331','2016-05-30 18:58:38.504355',NULL,1,2,3),(4,'2016-05-30 00:00:00.989855','2016-05-30 23:59:59.989878','2',NULL,'2016-05-30 20:10:36.002974','2016-05-30 20:10:36.003018',NULL,1,2,4),(5,'2016-05-30 00:00:00.279597','2016-05-30 23:59:59.279610','4',NULL,'2016-05-30 20:37:09.296541','2016-05-30 20:37:09.296585',NULL,1,2,8),(6,'2016-05-30 00:00:00.231182','2016-05-30 23:59:59.231195','First schedule',NULL,'2016-05-30 21:15:33.291525','2016-05-30 21:15:33.291571',NULL,3,2,9);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_rule`
--

LOCK TABLES `schedule_rule` WRITE;
/*!40000 ALTER TABLE `schedule_rule` DISABLE KEYS */;
INSERT INTO `schedule_rule` VALUES (2,'temp1','temp1','DAILY',NULL),(3,'1','1','DAILY',NULL),(4,'2','2','DAILY',NULL),(8,'4','4','DAILY',NULL),(9,'First schedule','First schedule','DAILY',NULL);
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
  `created_by_id` int(11) DEFAULT NULL,
  `organization_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`group_id`),
  KEY `created_by_id_25bf7d25606eb7cf_fk_authentication_userdetails_id` (`created_by_id`),
  KEY `a336d8d83dbde3af1e27c50bab159d86` (`organization_id`),
  CONSTRAINT `a336d8d83dbde3af1e27c50bab159d86` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `created_by_id_25bf7d25606eb7cf_fk_authentication_userdetails_id` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_group`
--

LOCK TABLES `screenManagement_group` WRITE;
/*!40000 ALTER TABLE `screenManagement_group` DISABLE KEYS */;
INSERT INTO `screenManagement_group` VALUES (1,'Group 1','First group','2016-05-29',1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_groupscreens`
--

LOCK TABLES `screenManagement_groupscreens` WRITE;
/*!40000 ALTER TABLE `screenManagement_groupscreens` DISABLE KEYS */;
INSERT INTO `screenManagement_groupscreens` VALUES (1,1,1,1);
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
  PRIMARY KEY (`screen_id`),
  UNIQUE KEY `unique_device_key_id` (`unique_device_key_id`),
  KEY `D67d42462e3f1c36ec77e9e9dc09390b` (`activated_by_id`),
  KEY `a7c1ba1e3d46eee1df95a619a8c2f227` (`owned_by_id`),
  KEY `scre_screen_calendar_id_58aceaff89f25de5_fk_schedule_calendar_id` (`screen_calendar_id`),
  KEY `screenManagement_screen_dc91ed4b` (`status_id`),
  KEY `screenManagement_screen_c7141997` (`city_id`),
  CONSTRAINT `D099a9619f8d384185c59ce135083230` FOREIGN KEY (`unique_device_key_id`) REFERENCES `screenManagement_screenactivationkey` (`screen_activation_id`),
  CONSTRAINT `D23b29036e98defa308670106fdeab4f` FOREIGN KEY (`status_id`) REFERENCES `screenManagement_screenstatus` (`screen_status_id`),
  CONSTRAINT `D67d42462e3f1c36ec77e9e9dc09390b` FOREIGN KEY (`activated_by_id`) REFERENCES `authentication_userdetails` (`id`),
  CONSTRAINT `a7c1ba1e3d46eee1df95a619a8c2f227` FOREIGN KEY (`owned_by_id`) REFERENCES `authentication_organization` (`organization_id`),
  CONSTRAINT `scre_screen_calendar_id_58aceaff89f25de5_fk_schedule_calendar_id` FOREIGN KEY (`screen_calendar_id`) REFERENCES `schedule_calendar` (`id`),
  CONSTRAINT `screenMa_city_id_6ada127b1914a468_fk_authentication_city_city_id` FOREIGN KEY (`city_id`) REFERENCES `authentication_city` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screen`
--

LOCK TABLES `screenManagement_screen` WRITE;
/*!40000 ALTER TABLE `screenManagement_screen` DISABLE KEYS */;
INSERT INTO `screenManagement_screen` VALUES (1,'jaydev android emulator',32,'16:9','1190*768','','2016-05-28 13:36:27.202897','PRIVATE',1,1,1,2,1,1),(2,'test',24,'16:9','1024*768','mount fort','2016-05-29 11:47:08.863168','PRIVATE',1,1,2,2,2,1);
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
INSERT INTO `screenManagement_screenactivationkey` VALUES (1,'a197cb391f0698e5','android emulator jay',1,0),(2,'1234567890','abc def',0,0);
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

-- Dump completed on 2016-05-31 11:29:52
