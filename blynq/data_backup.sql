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
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add city',7,'add_city'),(20,'Can change city',7,'change_city'),(21,'Can delete city',7,'delete_city'),(22,'Can add address',8,'add_address'),(23,'Can change address',8,'change_address'),(24,'Can delete address',8,'delete_address'),(25,'Can add organization',9,'add_organization'),(26,'Can change organization',9,'change_organization'),(27,'Can delete organization',9,'delete_organization'),(28,'Can add role',10,'add_role'),(29,'Can change role',10,'change_role'),(30,'Can delete role',10,'delete_role'),(31,'Can add user',11,'add_userdetails'),(32,'Can change user',11,'change_userdetails'),(33,'Can delete user',11,'delete_userdetails'),(34,'Can add screen status',12,'add_screenstatus'),(35,'Can change screen status',12,'change_screenstatus'),(36,'Can delete screen status',12,'delete_screenstatus'),(40,'Can add group',14,'add_group'),(41,'Can change group',14,'change_group'),(42,'Can delete group',14,'delete_group'),(43,'Can add screen specs',15,'add_screenspecs'),(44,'Can change screen specs',15,'change_screenspecs'),(45,'Can delete screen specs',15,'delete_screenspecs'),(46,'Can add organization screen',16,'add_organizationscreen'),(47,'Can change organization screen',16,'change_organizationscreen'),(48,'Can delete organization screen',16,'delete_organizationscreen'),(49,'Can add screen',17,'add_screen'),(50,'Can change screen',17,'change_screen'),(51,'Can delete screen',17,'delete_screen'),(52,'Can add content type',18,'add_contenttype'),(53,'Can change content type',18,'change_contenttype'),(54,'Can delete content type',18,'delete_contenttype'),(58,'Can add content',20,'add_content'),(59,'Can change content',20,'change_content'),(60,'Can delete content',20,'delete_content'),(61,'Can add playlist items',21,'add_playlistitems'),(62,'Can change playlist items',21,'change_playlistitems'),(63,'Can delete playlist items',21,'delete_playlistitems'),(64,'Can add playlist',22,'add_playlist'),(65,'Can change playlist',22,'change_playlist'),(66,'Can delete playlist',22,'delete_playlist'),(67,'Can add schedule',23,'add_schedule'),(68,'Can change schedule',23,'change_schedule'),(69,'Can delete schedule',23,'delete_schedule'),(70,'Can add event',24,'add_event'),(71,'Can change event',24,'change_event'),(72,'Can delete event',24,'delete_event'),(73,'Can add source',25,'add_source'),(74,'Can change source',25,'change_source'),(75,'Can delete source',25,'delete_source'),(76,'Can add thumbnail',26,'add_thumbnail'),(77,'Can change thumbnail',26,'change_thumbnail'),(78,'Can delete thumbnail',26,'delete_thumbnail'),(79,'Can add thumbnail dimensions',27,'add_thumbnaildimensions'),(80,'Can change thumbnail dimensions',27,'change_thumbnaildimensions'),(81,'Can delete thumbnail dimensions',27,'delete_thumbnaildimensions'),(82,'Can add Folder',28,'add_folder'),(83,'Can change Folder',28,'change_folder'),(84,'Can delete Folder',28,'delete_folder'),(85,'Can use directory listing',28,'can_use_directory_listing'),(86,'Can add folder permission',29,'add_folderpermission'),(87,'Can change folder permission',29,'change_folderpermission'),(88,'Can delete folder permission',29,'delete_folderpermission'),(89,'Can add file',30,'add_file'),(90,'Can change file',30,'change_file'),(91,'Can delete file',30,'delete_file'),(92,'Can add clipboard',31,'add_clipboard'),(93,'Can change clipboard',31,'change_clipboard'),(94,'Can delete clipboard',31,'delete_clipboard'),(95,'Can add clipboard item',32,'add_clipboarditem'),(96,'Can change clipboard item',32,'change_clipboarditem'),(97,'Can delete clipboard item',32,'delete_clipboarditem'),(98,'Can add image',33,'add_image'),(99,'Can change image',33,'change_image'),(100,'Can delete image',33,'delete_image');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$20000$OheAYidGFVmh$kndpFbifnw+QFpe/OiNHrs1Z/SS2Ou9VWhp8N8qbFaM=','2016-04-15 11:56:15.869682',1,'blynq','','','blynq@googlegroups.com',1,1,'2016-04-10 04:52:08.102966'),(3,'pbkdf2_sha256$20000$hYRk2vw3Qd3S$pHjgXCJR3iWlij2WE8d+/CnptH7CaInF846DLDQqpM8=','2016-04-13 02:26:23.623970',1,'nipun','nipun','edara','iitg.nipun@gmail.com',0,1,'2016-04-10 05:38:49.315257'),(5,'nishtnath',NULL,0,'sahruj','nipun','edara','sahrujviru@gmail.com',0,1,'2016-04-10 06:08:35.951219'),(6,'pbkdf2_sha256$20000$N1BFEkGoH8EU$6+L/gDHleXtO+GGzoWPG5J8EC01FCNy0bTK9ntmdHRw=','2016-04-10 11:21:51.214410',0,'kmpk123','kmpk','123','kmpk123@gmail.com',0,1,'2016-04-10 06:31:28.317982'),(7,'pbkdf2_sha256$20000$Rg2DKHFh7G02$6mX00ecYg93T9smWxLTJA9CxIOvuYMSYK85TfD8p+d0=',NULL,0,'abc','','','abc@gmail.com',0,1,'2016-04-10 11:21:13.164579'),(8,'pbkdf2_sha256$20000$MDZMFdo5ZvzY$9k9JPGWoWxzeX1k0fSdWFzsquqjKAnsphfW9JMP4QJc=',NULL,0,'jaydev','jaydev','k','jaydev@gmail.com',0,1,'2016-04-11 04:59:18.320907'),(9,'pbkdf2_sha256$20000$dYlFPgv7szhh$LqVEyiFoSwYOvSyyXfMIPEDECXBBM8IhUwxQhP/i8aA=','2016-04-11 06:21:59.456249',0,'abcdef','abc','def','abcdef@gmail.com',0,1,'2016-04-11 06:20:14.285474'),(10,'pbkdf2_sha256$20000$gPRDFHIFkPBn$tIPWd+vzNrDuYap41GNymzc6TWZJOi7sxSU3g4Spuqw=','2016-04-11 07:28:19.167752',0,'asdf','asdf','123','asdf@gmail.com',0,1,'2016-04-11 07:28:04.071170');
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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `building_name` varchar(100) NOT NULL,
  `address_line1` varchar(100) NOT NULL,
  `address_line2` varchar(100) NOT NULL,
  `area` varchar(100) NOT NULL,
  `landmark` varchar(100) NOT NULL,
  `pincode` int(11) NOT NULL,
  `city_id` int(11) NOT NULL,
  `added_by_id` int(11),
  PRIMARY KEY (`id`),
  UNIQUE KEY `authentication_address_building_name_307a710555774b15_uniq` (`building_name`,`added_by_id`),
  KEY `authentication_address_c7141997` (`city_id`),
  KEY `authentication_address_0c5d7d4e` (`added_by_id`),
  CONSTRAINT `authenticatio_city_id_392ccb660d3eb8f0_fk_authentication_city_id` FOREIGN KEY (`city_id`) REFERENCES `authentication_city` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_address`
--

LOCK TABLES `authentication_address` WRITE;
/*!40000 ALTER TABLE `authentication_address` DISABLE KEYS */;
INSERT INTO `authentication_address` VALUES (1,'bangalore central mall','near flyover','beside outer ring road','bellandur','Flyover',560103,1,NULL),(2,'abc','def','def','bellandur','ORR',560103,1,NULL),(3,'oceanus freesia enclave','asdf','bellandur main road','bellandur','Ramdev medicals',560103,1,3);
/*!40000 ALTER TABLE `authentication_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_city`
--

DROP TABLE IF EXISTS `authentication_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_city`
--

LOCK TABLES `authentication_city` WRITE;
/*!40000 ALTER TABLE `authentication_city` DISABLE KEYS */;
INSERT INTO `authentication_city` VALUES (1,'Bengaluru','karnataka');
/*!40000 ALTER TABLE `authentication_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_organization`
--

DROP TABLE IF EXISTS `authentication_organization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `website` varchar(100) NOT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `authenti_address_id_6ad93a85dcf06e8_fk_authentication_address_id` (`address_id`),
  CONSTRAINT `authenti_address_id_6ad93a85dcf06e8_fk_authentication_address_id` FOREIGN KEY (`address_id`) REFERENCES `authentication_address` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_organization`
--

LOCK TABLES `authentication_organization` WRITE;
/*!40000 ALTER TABLE `authentication_organization` DISABLE KEYS */;
INSERT INTO `authentication_organization` VALUES (1,'Blynq Pvt Ltd','www.blynq.in','8277121319',NULL);
/*!40000 ALTER TABLE `authentication_organization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_role`
--

DROP TABLE IF EXISTS `authentication_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  `role_description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_role`
--

LOCK TABLES `authentication_role` WRITE;
/*!40000 ALTER TABLE `authentication_role` DISABLE KEYS */;
INSERT INTO `authentication_role` VALUES (1,'viewer','User who can just view content'),(2,'scheduler','User who can view as well as schedule content on the screens'),(3,'uploader','User who can view, schedule as well as upload new content'),(4,'manager','User who can upload+schedule+ modify user roles for that company');
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
  KEY `D346c2a9c17d9d15bfde61c10156cf02` (`organization_id`),
  KEY `authenticatio_role_id_44612207d2201d34_fk_authentication_role_id` (`role_id`),
  CONSTRAINT `D346c2a9c17d9d15bfde61c10156cf02` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`id`),
  CONSTRAINT `authenticatio_role_id_44612207d2201d34_fk_authentication_role_id` FOREIGN KEY (`role_id`) REFERENCES `authentication_role` (`id`),
  CONSTRAINT `authentication_user_user_ptr_id_70f39c7da29ecb96_fk_auth_user_id` FOREIGN KEY (`user_ptr_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_userdetails`
--

LOCK TABLES `authentication_userdetails` WRITE;
/*!40000 ALTER TABLE `authentication_userdetails` DISABLE KEYS */;
INSERT INTO `authentication_userdetails` VALUES (3,'944080',1,4),(5,'944080',1,4),(6,'944080',1,4),(8,'1234567890',1,3),(9,'1234567890',1,1),(10,'1345678',1,1);
/*!40000 ALTER TABLE `authentication_userdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contentManagement_contenttype`
--

DROP TABLE IF EXISTS `contentManagement_contenttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentManagement_contenttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(3) NOT NULL,
  `fileExtension` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
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
-- Table structure for table `contentManagement_folder`
--

DROP TABLE IF EXISTS `contentManagement_folder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contentManagement_folder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `dummy_content_folder` tinyint(1) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `conten_parent_id_27da606267c6f79f_fk_contentManagement_folder_id` (`parent_id`),
  KEY `D81490e4ba595b4c795e8cff1f4d11eb` (`owner_id`),
  CONSTRAINT `D81490e4ba595b4c795e8cff1f4d11eb` FOREIGN KEY (`owner_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `conten_parent_id_27da606267c6f79f_fk_contentManagement_folder_id` FOREIGN KEY (`parent_id`) REFERENCES `contentManagement_folder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contentManagement_folder`
--

LOCK TABLES `contentManagement_folder` WRITE;
/*!40000 ALTER TABLE `contentManagement_folder` DISABLE KEYS */;
/*!40000 ALTER TABLE `contentManagement_folder` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-04-10 04:54:44.624773','1','viewer',1,'',10,1),(2,'2016-04-10 04:54:52.374826','2','scheduler',1,'',10,1),(3,'2016-04-10 04:54:59.029471','3','uploader',1,'',10,1),(4,'2016-04-10 04:55:06.892614','4','manager',1,'',10,1),(5,'2016-04-10 04:55:37.059045','1','Blynq Pvt Ltd',1,'',9,1),(6,'2016-04-11 09:23:26.798518','1','ScreenSpecs object',1,'',15,1),(7,'2016-04-11 09:51:40.085932','1','City object',1,'',7,1),(8,'2016-04-11 09:52:19.645464','1','Address object',1,'',8,1),(10,'2016-04-11 10:03:37.504580','1','active',1,'',12,1),(11,'2016-04-11 10:05:06.279278','2','abc, bellandur, Bengaluru',1,'',8,1),(13,'2016-04-11 10:05:52.158022','2','active',1,'',12,1),(14,'2016-04-11 10:09:04.243012','1','screen 1',1,'',17,1),(15,'2016-04-11 10:11:31.290590','2','screen 2',1,'',17,1),(16,'2016-04-11 10:12:44.433362','2','screen 2',2,'Changed status.',17,1),(17,'2016-04-11 10:13:07.813934','1','active',3,'',12,1),(18,'2016-04-11 10:13:50.074993','1','screen 1',2,'Changed business_type.',17,1),(20,'2016-04-12 11:52:21.246651','3','Unactivated',1,'',12,1),(21,'2016-04-12 11:52:40.362468','4','Online',1,'',12,1),(22,'2016-04-12 11:53:06.409097','5','Offline',1,'',12,1),(23,'2016-04-12 11:53:35.598468','6','Idle',1,'',12,1),(24,'2016-04-12 11:54:51.052972','1','screen 1',2,'Changed business_type and status.',17,1),(25,'2016-04-12 11:55:04.538215','2','screen 2',2,'Changed business_type and status.',17,1),(26,'2016-04-12 11:55:26.273660','2','active',3,'',12,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(8,'authentication','address'),(7,'authentication','city'),(9,'authentication','organization'),(10,'authentication','role'),(11,'authentication','userdetails'),(20,'contentManagement','content'),(18,'contentManagement','contenttype'),(5,'contenttypes','contenttype'),(25,'easy_thumbnails','source'),(26,'easy_thumbnails','thumbnail'),(27,'easy_thumbnails','thumbnaildimensions'),(31,'filer','clipboard'),(32,'filer','clipboarditem'),(30,'filer','file'),(28,'filer','folder'),(29,'filer','folderpermission'),(33,'filer','image'),(22,'playlistManagement','playlist'),(21,'playlistManagement','playlistitems'),(24,'scheduleManagement','event'),(23,'scheduleManagement','schedule'),(14,'screenManagement','group'),(16,'screenManagement','organizationscreen'),(17,'screenManagement','screen'),(15,'screenManagement','screenspecs'),(12,'screenManagement','screenstatus'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-04-10 04:51:37.188744'),(2,'auth','0001_initial','2016-04-10 04:51:37.758972'),(3,'admin','0001_initial','2016-04-10 04:51:37.915210'),(4,'contenttypes','0002_remove_content_type_name','2016-04-10 04:51:38.031647'),(5,'auth','0002_alter_permission_name_max_length','2016-04-10 04:51:38.092351'),(6,'auth','0003_alter_user_email_max_length','2016-04-10 04:51:38.176661'),(7,'auth','0004_alter_user_username_opts','2016-04-10 04:51:38.193122'),(8,'auth','0005_alter_user_last_login_null','2016-04-10 04:51:38.254328'),(9,'auth','0006_require_contenttypes_0002','2016-04-10 04:51:38.260170'),(10,'sessions','0001_initial','2016-04-10 04:51:38.315816'),(11,'authentication','0001_initial','2016-04-10 04:54:05.126916'),(12,'contentManagement','0001_initial','2016-04-10 04:54:06.003701'),(13,'playlistManagement','0001_initial','2016-04-10 04:54:06.387775'),(14,'screenManagement','0001_initial','2016-04-10 04:54:07.704416'),(15,'scheduleManagement','0001_initial','2016-04-10 04:54:08.267686'),(16,'authentication','0002_auto_20160411_0427','2016-04-11 04:27:32.707883'),(17,'authentication','0003_auto_20160412_0344','2016-04-12 03:45:08.144452'),(18,'screenManagement','0002_auto_20160412_0344','2016-04-12 03:45:09.715110'),(19,'screenManagement','0003_auto_20160412_0409','2016-04-12 04:09:41.245378'),(20,'screenManagement','0004_auto_20160412_0850','2016-04-12 08:50:08.302403'),(21,'screenManagement','0005_auto_20160412_1055','2016-04-12 10:56:05.655861'),(22,'authentication','0004_auto_20160412_1349','2016-04-12 13:49:19.857183'),(23,'screenManagement','0002_screen_activated_by','2016-04-13 10:07:00.535854'),(24,'screenManagement','0003_auto_20160413_1116','2016-04-13 11:16:46.926098'),(25,'screenManagement','0004_auto_20160414_0953','2016-04-14 09:54:02.682464'),(26,'screenManagement','0005_auto_20160414_1331','2016-04-14 13:31:27.748029'),(27,'easy_thumbnails','0001_initial','2016-04-15 03:48:57.018678'),(28,'easy_thumbnails','0002_thumbnaildimensions','2016-04-15 03:48:57.122555'),(29,'filer','0001_initial','2016-04-15 03:48:58.837148'),(30,'filer','0002_auto_20150606_2003','2016-04-15 03:48:58.965404'),(31,'authentication','0002_auto_20160415_0935','2016-04-15 09:40:34.041531'),(32,'contentManagement','0002_auto_20160415_0935','2016-04-15 09:40:34.180698'),(33,'contentManagement','0003_auto_20160415_1130','2016-04-15 11:30:30.794995'),(34,'contentManagement','0002_content_is_folder','2016-04-15 18:06:13.108479'),(35,'contentManagement','0003_auto_20160415_1813','2016-04-15 18:13:04.415756'),(36,'contentManagement','0002_auto_20160415_1833','2016-04-15 18:33:42.223813');
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
INSERT INTO `django_session` VALUES ('9x7h3jl9i6emfh8ll1p54ke4j1ahzbtn','ZTZjNmI0NThlNjdhNDcyNGZlNzA4NTIxM2ZlMTNiZTc0MmVhMjQ0Mjp7Il9hdXRoX3VzZXJfaGFzaCI6IjZmOTA3MDZmZTA1N2ExYTVkYzViMTBhMWFhYTA5N2Q3Zjg1MGFmMzciLCJmaWxlcl9sYXN0X2ZvbGRlcl9pZCI6bnVsbCwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2016-04-29 11:56:34.407007');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_source`
--

DROP TABLE IF EXISTS `easy_thumbnails_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `storage_hash` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `modified` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_source_storage_hash_40116450c1e4f2ed_uniq` (`storage_hash`,`name`),
  KEY `easy_thumbnails_source_b454e115` (`storage_hash`),
  KEY `easy_thumbnails_source_b068931c` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_source`
--

LOCK TABLES `easy_thumbnails_source` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_source` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnail`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_thumbnail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `storage_hash` varchar(40) NOT NULL,
  `name` varchar(255) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `source_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `easy_thumbnails_thumbnail_storage_hash_66cc758d07ef9fce_uniq` (`storage_hash`,`name`,`source_id`),
  KEY `easy_thu_source_id_50b260de7106e1b7_fk_easy_thumbnails_source_id` (`source_id`),
  KEY `easy_thumbnails_thumbnail_b454e115` (`storage_hash`),
  KEY `easy_thumbnails_thumbnail_b068931c` (`name`),
  CONSTRAINT `easy_thu_source_id_50b260de7106e1b7_fk_easy_thumbnails_source_id` FOREIGN KEY (`source_id`) REFERENCES `easy_thumbnails_source` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnail`
--

LOCK TABLES `easy_thumbnails_thumbnail` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `easy_thumbnails_thumbnaildimensions`
--

DROP TABLE IF EXISTS `easy_thumbnails_thumbnaildimensions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `easy_thumbnails_thumbnaildimensions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thumbnail_id` int(11) NOT NULL,
  `width` int(10) unsigned DEFAULT NULL,
  `height` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `thumbnail_id` (`thumbnail_id`),
  CONSTRAINT `ea_thumbnail_id_29ad34faceb3c17c_fk_easy_thumbnails_thumbnail_id` FOREIGN KEY (`thumbnail_id`) REFERENCES `easy_thumbnails_thumbnail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easy_thumbnails_thumbnaildimensions`
--

LOCK TABLES `easy_thumbnails_thumbnaildimensions` WRITE;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnaildimensions` DISABLE KEYS */;
/*!40000 ALTER TABLE `easy_thumbnails_thumbnaildimensions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_clipboard`
--

DROP TABLE IF EXISTS `filer_clipboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_clipboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `filer_clipboard_e8701ad4` (`user_id`),
  CONSTRAINT `filer_clipboard_user_id_2b30c76f2cd235df_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_clipboard`
--

LOCK TABLES `filer_clipboard` WRITE;
/*!40000 ALTER TABLE `filer_clipboard` DISABLE KEYS */;
INSERT INTO `filer_clipboard` VALUES (1,1);
/*!40000 ALTER TABLE `filer_clipboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_clipboarditem`
--

DROP TABLE IF EXISTS `filer_clipboarditem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_clipboarditem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clipboard_id` int(11) NOT NULL,
  `file_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `filer_clipbo_clipboard_id_335d159e1aea2cdc_fk_filer_clipboard_id` (`clipboard_id`),
  KEY `filer_clipboarditem_814552b9` (`file_id`),
  CONSTRAINT `filer_clipbo_clipboard_id_335d159e1aea2cdc_fk_filer_clipboard_id` FOREIGN KEY (`clipboard_id`) REFERENCES `filer_clipboard` (`id`),
  CONSTRAINT `filer_clipboarditem_file_id_7b1b6a14b5a3f2b1_fk_filer_file_id` FOREIGN KEY (`file_id`) REFERENCES `filer_file` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_clipboarditem`
--

LOCK TABLES `filer_clipboarditem` WRITE;
/*!40000 ALTER TABLE `filer_clipboarditem` DISABLE KEYS */;
/*!40000 ALTER TABLE `filer_clipboarditem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_file`
--

DROP TABLE IF EXISTS `filer_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(255) DEFAULT NULL,
  `_file_size` int(11) DEFAULT NULL,
  `sha1` varchar(40) NOT NULL,
  `has_all_mandatory_data` tinyint(1) NOT NULL,
  `original_filename` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `uploaded_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `folder_id` int(11),
  `owner_id` int(11),
  `polymorphic_ctype_id` int(11),
  PRIMARY KEY (`id`),
  KEY `filer_file_a8a44dbb` (`folder_id`),
  KEY `filer_file_5e7b1936` (`owner_id`),
  KEY `filer_file_d3e32c49` (`polymorphic_ctype_id`),
  CONSTRAINT `filer_file_folder_id_24318dda71f59785_fk_filer_folder_id` FOREIGN KEY (`folder_id`) REFERENCES `filer_folder` (`id`),
  CONSTRAINT `filer_file_owner_id_67317c663ea33283_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `polymorphic_ctype_id_37b6c9e9cb7a323a_fk_django_content_type_id` FOREIGN KEY (`polymorphic_ctype_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_file`
--

LOCK TABLES `filer_file` WRITE;
/*!40000 ALTER TABLE `filer_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `filer_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_folder`
--

DROP TABLE IF EXISTS `filer_folder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_folder` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `modified_at` datetime(6) NOT NULL,
  `lft` int(10) unsigned NOT NULL,
  `rght` int(10) unsigned NOT NULL,
  `tree_id` int(10) unsigned NOT NULL,
  `level` int(10) unsigned NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `filer_folder_parent_id_30ad83e34d901e49_uniq` (`parent_id`,`name`),
  KEY `filer_folder_owner_id_6527f5f13a76f3ed_fk_auth_user_id` (`owner_id`),
  KEY `filer_folder_caf7cc51` (`lft`),
  KEY `filer_folder_3cfbd988` (`rght`),
  KEY `filer_folder_656442a0` (`tree_id`),
  KEY `filer_folder_c9e9a848` (`level`),
  CONSTRAINT `filer_folder_owner_id_6527f5f13a76f3ed_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `filer_folder_parent_id_4170098ac31c2cbf_fk_filer_folder_id` FOREIGN KEY (`parent_id`) REFERENCES `filer_folder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_folder`
--

LOCK TABLES `filer_folder` WRITE;
/*!40000 ALTER TABLE `filer_folder` DISABLE KEYS */;
/*!40000 ALTER TABLE `filer_folder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_folderpermission`
--

DROP TABLE IF EXISTS `filer_folderpermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_folderpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` smallint(6) NOT NULL,
  `everybody` tinyint(1) NOT NULL,
  `can_edit` smallint(6) DEFAULT NULL,
  `can_read` smallint(6) DEFAULT NULL,
  `can_add_children` smallint(6) DEFAULT NULL,
  `folder_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `filer_folderpermis_folder_id_442a5347ee209a98_fk_filer_folder_id` (`folder_id`),
  KEY `filer_folderpermissio_group_id_7c2389ac07ebbde2_fk_auth_group_id` (`group_id`),
  KEY `filer_folderpermission_user_id_7c6e1a7187a0f15b_fk_auth_user_id` (`user_id`),
  CONSTRAINT `filer_folderpermis_folder_id_442a5347ee209a98_fk_filer_folder_id` FOREIGN KEY (`folder_id`) REFERENCES `filer_folder` (`id`),
  CONSTRAINT `filer_folderpermissio_group_id_7c2389ac07ebbde2_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `filer_folderpermission_user_id_7c6e1a7187a0f15b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_folderpermission`
--

LOCK TABLES `filer_folderpermission` WRITE;
/*!40000 ALTER TABLE `filer_folderpermission` DISABLE KEYS */;
/*!40000 ALTER TABLE `filer_folderpermission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filer_image`
--

DROP TABLE IF EXISTS `filer_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `filer_image` (
  `file_ptr_id` int(11) NOT NULL,
  `_height` int(11) DEFAULT NULL,
  `_width` int(11) DEFAULT NULL,
  `date_taken` datetime(6) DEFAULT NULL,
  `default_alt_text` varchar(255) DEFAULT NULL,
  `default_caption` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `must_always_publish_author_credit` tinyint(1) NOT NULL,
  `must_always_publish_copyright` tinyint(1) NOT NULL,
  `subject_location` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`file_ptr_id`),
  CONSTRAINT `filer_image_file_ptr_id_1dde9ad32bce39a6_fk_filer_file_id` FOREIGN KEY (`file_ptr_id`) REFERENCES `filer_file` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filer_image`
--

LOCK TABLES `filer_image` WRITE;
/*!40000 ALTER TABLE `filer_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `filer_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlistManagement_playlist`
--

DROP TABLE IF EXISTS `playlistManagement_playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlistManagement_playlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `last_updated_by_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `D50229839cd0cf7d84abc44588a9db0d` (`created_by_id`),
  KEY `c98e25b8402d78f8544a252ae221ba89` (`last_updated_by_id`),
  CONSTRAINT `D50229839cd0cf7d84abc44588a9db0d` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `c98e25b8402d78f8544a252ae221ba89` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlist`
--

LOCK TABLES `playlistManagement_playlist` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlistManagement_playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlistManagement_playlistitems`
--

DROP TABLE IF EXISTS `playlistManagement_playlistitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlistManagement_playlistitems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL,
  `display_time` int(11) NOT NULL,
  `folder_id` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `playli_folder_id_369bb9a40f627f48_fk_contentManagement_folder_id` (`folder_id`),
  KEY `p_playlist_id_21a128d242be2db4_fk_playlistManagement_playlist_id` (`playlist_id`),
  CONSTRAINT `p_playlist_id_21a128d242be2db4_fk_playlistManagement_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`id`),
  CONSTRAINT `playli_folder_id_369bb9a40f627f48_fk_contentManagement_folder_id` FOREIGN KEY (`folder_id`) REFERENCES `contentManagement_folder` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlistManagement_playlistitems`
--

LOCK TABLES `playlistManagement_playlistitems` WRITE;
/*!40000 ALTER TABLE `playlistManagement_playlistitems` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlistManagement_playlistitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_event`
--

DROP TABLE IF EXISTS `scheduleManagement_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `schedule_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scheduleManagement_event_9bc70bb9` (`schedule_id`),
  CONSTRAINT `s_schedule_id_2e6322707b09983e_fk_scheduleManagement_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_event`
--

LOCK TABLES `scheduleManagement_event` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduleManagement_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_schedule`
--

DROP TABLE IF EXISTS `scheduleManagement_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_time` datetime(6) NOT NULL,
  `last_updated_time` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `last_updated_by_id` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `b405690da41b1b8e66ba521e8f2675f6` (`created_by_id`),
  KEY `D0008ec854458223fc0440e7f59934e8` (`last_updated_by_id`),
  KEY `s_playlist_id_27974a8b8ad55599_fk_playlistManagement_playlist_id` (`playlist_id`),
  CONSTRAINT `D0008ec854458223fc0440e7f59934e8` FOREIGN KEY (`last_updated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `b405690da41b1b8e66ba521e8f2675f6` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `s_playlist_id_27974a8b8ad55599_fk_playlistManagement_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlistManagement_playlist` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedule`
--

LOCK TABLES `scheduleManagement_schedule` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduleManagement_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scheduleManagement_schedule_screens`
--

DROP TABLE IF EXISTS `scheduleManagement_schedule_screens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scheduleManagement_schedule_screens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `schedule_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `schedule_id` (`schedule_id`,`group_id`),
  KEY `scheduleMa_group_id_46d317ee2af5323_fk_screenManagement_group_id` (`group_id`),
  CONSTRAINT `sc_schedule_id_a2ba00561d3af8e_fk_scheduleManagement_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `scheduleManagement_schedule` (`id`),
  CONSTRAINT `scheduleMa_group_id_46d317ee2af5323_fk_screenManagement_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scheduleManagement_schedule_screens`
--

LOCK TABLES `scheduleManagement_schedule_screens` WRITE;
/*!40000 ALTER TABLE `scheduleManagement_schedule_screens` DISABLE KEYS */;
/*!40000 ALTER TABLE `scheduleManagement_schedule_screens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_group`
--

DROP TABLE IF EXISTS `screenManagement_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(100) NOT NULL,
  `description` longtext,
  `created_on` date NOT NULL,
  `dummy_screen_group` tinyint(1) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `organization_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `f4d416adc879a6e27bc401a773527249` (`created_by_id`),
  KEY `d74576a1123c5f825d60cb3998c8ab2a` (`organization_id`),
  CONSTRAINT `d74576a1123c5f825d60cb3998c8ab2a` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`id`),
  CONSTRAINT `f4d416adc879a6e27bc401a773527249` FOREIGN KEY (`created_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_group`
--

LOCK TABLES `screenManagement_group` WRITE;
/*!40000 ALTER TABLE `screenManagement_group` DISABLE KEYS */;
INSERT INTO `screenManagement_group` VALUES (1,'shopping malls','This group has all the screens placed in shopping malls.','2016-04-13',0,3,1),(2,'9th floor','Screen placed on 9th floor','2016-04-13',0,3,1);
/*!40000 ALTER TABLE `screenManagement_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_organizationscreen`
--

DROP TABLE IF EXISTS `screenManagement_organizationscreen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_organizationscreen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `time_slot_valid` tinyint(1) NOT NULL,
  `time_slot` int(11) DEFAULT NULL,
  `organization_id` int(11) NOT NULL,
  `screen_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `f62945ee7691263de5242f772206c282` (`organization_id`),
  KEY `screenManagement_organizationscreen_e4ec8585` (`screen_id`),
  CONSTRAINT `f62945ee7691263de5242f772206c282` FOREIGN KEY (`organization_id`) REFERENCES `authentication_organization` (`id`),
  CONSTRAINT `screenM_screen_id_7489f5e0c013537a_fk_screenManagement_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_organizationscreen`
--

LOCK TABLES `screenManagement_organizationscreen` WRITE;
/*!40000 ALTER TABLE `screenManagement_organizationscreen` DISABLE KEYS */;
/*!40000 ALTER TABLE `screenManagement_organizationscreen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screen`
--

DROP TABLE IF EXISTS `screenManagement_screen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `screen_name` varchar(100) NOT NULL,
  `activation_key` varchar(16) NOT NULL,
  `activated_on` date DEFAULT NULL,
  `business_type` varchar(20) NOT NULL,
  `location_id` int(11) NOT NULL,
  `placed_by_id` int(11) DEFAULT NULL,
  `specifications_id` int(11) NOT NULL,
  `status_id` int(11) NOT NULL,
  `activated_by_id` int(11),
  PRIMARY KEY (`id`),
  KEY `screen_location_id_3f068de9f683308c_fk_authentication_address_id` (`location_id`),
  KEY `screenManagement_screen_e0be6253` (`specifications_id`),
  KEY `screenManagement_screen_dc91ed4b` (`status_id`),
  KEY `placed_by_id_73963cfeb4e5cc15_fk_authentication_organization_id` (`placed_by_id`),
  KEY `screenManagement_screen_d5b8d1c2` (`activated_by_id`),
  CONSTRAINT `D88c12cf584bd9ec0769c0e380dd6d95` FOREIGN KEY (`specifications_id`) REFERENCES `screenManagement_screenspecs` (`id`),
  CONSTRAINT `ebc63bdd0f179da0d15ee30f124ea0e0` FOREIGN KEY (`activated_by_id`) REFERENCES `authentication_userdetails` (`user_ptr_id`),
  CONSTRAINT `placed_by_id_73963cfeb4e5cc15_fk_authentication_organization_id` FOREIGN KEY (`placed_by_id`) REFERENCES `authentication_organization` (`id`),
  CONSTRAINT `s_status_id_7e5335d768560aa1_fk_screenManagement_screenstatus_id` FOREIGN KEY (`status_id`) REFERENCES `screenManagement_screenstatus` (`id`),
  CONSTRAINT `screen_location_id_3f068de9f683308c_fk_authentication_address_id` FOREIGN KEY (`location_id`) REFERENCES `authentication_address` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screen`
--

LOCK TABLES `screenManagement_screen` WRITE;
/*!40000 ALTER TABLE `screenManagement_screen` DISABLE KEYS */;
INSERT INTO `screenManagement_screen` VALUES (1,'screen 1','ASDF1234','2016-04-11','PRIVATE',2,1,1,3,NULL),(2,'screen 2','asdf123333','2016-04-11','PRIVATE',1,1,1,3,NULL),(3,'screen abc','',NULL,'PRIVATE',1,1,1,3,NULL),(4,'Screen 22','',NULL,'PRIVATE',1,1,1,3,NULL),(5,'nipun','',NULL,'PRIVATE',1,1,1,3,NULL),(6,'shopping 9th floor','',NULL,'PRIVATE',3,1,2,3,NULL),(7,'dominos','',NULL,'PRIVATE',1,1,2,3,NULL),(8,'dominos12','',NULL,'PRIVATE',1,1,2,3,NULL);
/*!40000 ALTER TABLE `screenManagement_screen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screen_groups`
--

DROP TABLE IF EXISTS `screenManagement_screen_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screen_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `screen_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `screen_id` (`screen_id`,`group_id`),
  KEY `screenMan_group_id_4dc0b1699266de69_fk_screenManagement_group_id` (`group_id`),
  CONSTRAINT `screenM_screen_id_113a154b52f5ae05_fk_screenManagement_screen_id` FOREIGN KEY (`screen_id`) REFERENCES `screenManagement_screen` (`id`),
  CONSTRAINT `screenMan_group_id_4dc0b1699266de69_fk_screenManagement_group_id` FOREIGN KEY (`group_id`) REFERENCES `screenManagement_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screen_groups`
--

LOCK TABLES `screenManagement_screen_groups` WRITE;
/*!40000 ALTER TABLE `screenManagement_screen_groups` DISABLE KEYS */;
INSERT INTO `screenManagement_screen_groups` VALUES (1,8,1);
/*!40000 ALTER TABLE `screenManagement_screen_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screenspecs`
--

DROP TABLE IF EXISTS `screenManagement_screenspecs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screenspecs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand` varchar(50) NOT NULL,
  `model_num` varchar(50) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `dimensions` varchar(50) DEFAULT NULL,
  `resolution` varchar(20) DEFAULT NULL,
  `display_type` varchar(10) DEFAULT NULL,
  `screen_size` int(11) NOT NULL,
  `aspect_ratio` varchar(20) DEFAULT NULL,
  `contrast_ratio` varchar(20) DEFAULT NULL,
  `wattage` int(11) DEFAULT NULL,
  `additional_details` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `screenManagement_screenspecs_brand_3dc574781c54ace9_uniq` (`brand`,`model_num`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenspecs`
--

LOCK TABLES `screenManagement_screenspecs` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenspecs` DISABLE KEYS */;
INSERT INTO `screenManagement_screenspecs` VALUES (1,'Samsung','ABCDEF',12,'100*25*25','1744*899','LED',32,'16:9','null',65,'null'),(2,'AOC','AOC23445',10,'177*177*177','1850*977','LED',32,'16:9','25:4',100,'No more details');
/*!40000 ALTER TABLE `screenManagement_screenspecs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `screenManagement_screenstatus`
--

DROP TABLE IF EXISTS `screenManagement_screenstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `screenManagement_screenstatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `screenManagement_screenstatus_status_name_2008e8e81bd1bcf3_uniq` (`status_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `screenManagement_screenstatus`
--

LOCK TABLES `screenManagement_screenstatus` WRITE;
/*!40000 ALTER TABLE `screenManagement_screenstatus` DISABLE KEYS */;
INSERT INTO `screenManagement_screenstatus` VALUES (3,'Unactivated','The screen is not activated using the activation key.'),(4,'Online','The screen is online and is displaying content.'),(5,'Offline','The screen is either down or not connected to the internet.'),(6,'Idle','The screen is on but there is no active schedule being displayed right now.');
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

-- Dump completed on 2016-04-16  0:20:35
