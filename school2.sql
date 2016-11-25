-- MySQL dump 10.13  Distrib 5.7.12, for Linux (x86_64)
--
-- Host: localhost    Database: school2
-- ------------------------------------------------------
-- Server version	5.7.12-0ubuntu1

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
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class` (
  `class_id` int(11) NOT NULL,
  `class` varchar(15) DEFAULT NULL,
  `room` int(11) DEFAULT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'nursery',1),(2,'lkg',2),(3,'hkg',3),(4,'1',4),(5,'2',5),(6,'3',6),(7,'4',7),(8,'5',8),(9,'6',9),(10,'7',10),(11,'8',11),(12,'9',12),(13,'10',13),(14,'11',14),(15,'12',15);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_going_on`
--

DROP TABLE IF EXISTS `class_going_on`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `class_going_on` (
  `class_going_on_id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_type` varchar(15) DEFAULT NULL,
  `highest_marks` int(11) DEFAULT NULL,
  `course_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`class_going_on_id`),
  KEY `course_id` (`course_id`),
  KEY `class_id` (`class_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `class_going_on_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `class_going_on_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `class_going_on_ibfk_3` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_going_on`
--

LOCK TABLES `class_going_on` WRITE;
/*!40000 ALTER TABLE `class_going_on` DISABLE KEYS */;
INSERT INTO `class_going_on` VALUES (26,'quarterly',NULL,1,8,1),(27,'halfyearly',NULL,1,8,1),(28,'final',NULL,1,8,1),(29,'quarterly',NULL,2,8,1),(30,'halfyearly',NULL,2,8,1),(31,'final',NULL,2,8,1),(32,'quarterly',NULL,3,8,1),(33,'halfyearly',NULL,3,8,1),(34,'final',NULL,3,8,1),(35,'quarterly',NULL,14,8,2),(36,'halfyearly',NULL,14,8,2),(37,'final',NULL,14,8,2);
/*!40000 ALTER TABLE `class_going_on` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `syllabus` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'english',NULL),(2,'hindi',NULL),(3,'maths',NULL),(4,'physics',NULL),(5,'chemistry',NULL),(6,'biology',NULL),(7,'history',NULL),(8,'civics',NULL),(9,'geography',NULL),(10,'computer',NULL),(11,'sanskrit',NULL),(12,'social science',NULL),(13,'science',NULL),(14,'drawing',NULL),(15,'moral science',NULL),(16,'general knowledge',NULL),(17,'physical education',NULL),(18,'environmental studies',NULL),(19,'english dictation',NULL),(20,'hindi dictation',NULL),(21,'maths dodging',NULL),(22,'physical education',NULL);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `faculty` (
  `faculty_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` bigint(20) NOT NULL,
  PRIMARY KEY (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Seema Sharma','seemasharma@gmail.com',9999999999),(2,'Vandana Rana','vandanarana@gmail.com',9879456789);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_going_on_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `feedback` varchar(200) NOT NULL,
  PRIMARY KEY (`feedback_id`),
  KEY `class_going_on_id` (`class_going_on_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`class_going_on_id`) REFERENCES `class_going_on` (`class_going_on_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `feedback_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=467 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (466,26,1,'Excellent');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mark`
--

DROP TABLE IF EXISTS `mark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mark` (
  `mark_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_going_on_id` int(11) NOT NULL,
  `self_mark` int(11) NOT NULL,
  `exam_type` varchar(15) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`mark_id`),
  KEY `class_going_on_id` (`class_going_on_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `mark_ibfk_1` FOREIGN KEY (`class_going_on_id`) REFERENCES `class_going_on` (`class_going_on_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mark_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=481 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mark`
--

LOCK TABLES `mark` WRITE;
/*!40000 ALTER TABLE `mark` DISABLE KEYS */;
INSERT INTO `mark` VALUES (467,35,99,'quarterly',1),(468,35,98,'quarterly',2),(469,35,94,'quarterly',3),(470,36,94,'halfyearly',3),(471,37,94,'final',3),(472,37,94,'final',2),(473,36,94,'halfyearly',2),(474,36,94,'halfyearly',1),(475,37,99,'final',1),(476,32,60,'quarterly',1),(477,32,60,'quarterly',2),(478,34,60,'final',2),(479,33,60,'halfyearly',2),(480,33,60,'halfyearly',3);
/*!40000 ALTER TABLE `mark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notice`
--

DROP TABLE IF EXISTS `notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notice` (
  `notice_id` int(11) NOT NULL AUTO_INCREMENT,
  `info` varchar(1000) NOT NULL,
  `class_id` int(11) NOT NULL,
  `faculty_id` int(11) NOT NULL,
  PRIMARY KEY (`notice_id`),
  KEY `class_id` (`class_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `notice_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `notice_ibfk_2` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notice`
--

LOCK TABLES `notice` WRITE;
/*!40000 ALTER TABLE `notice` DISABLE KEYS */;
INSERT INTO `notice` VALUES (26,'14/07/16 will be a holiday',8,1),(27,'5 + x = 7*x .solve x ?',8,1);
/*!40000 ALTER TABLE `notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` bigint(20) NOT NULL,
  `class_id` int(11) NOT NULL,
  PRIMARY KEY (`student_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`class_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Akash Gupta','akashgupta@gmail.com',9999999999,8),(2,'Anant Dadu','anantdadu@gmail.com',9898989898,8),(3,'Tanya Jha','tanyajha@gmail.com',9494949494,8);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_slot`
--

DROP TABLE IF EXISTS `time_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_slot` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT,
  `day` varchar(10) NOT NULL,
  `period` varchar(5) NOT NULL,
  `class_going_on_id` int(11) NOT NULL,
  PRIMARY KEY (`t_id`),
  KEY `class_going_on_id` (`class_going_on_id`),
  CONSTRAINT `time_slot_ibfk_1` FOREIGN KEY (`class_going_on_id`) REFERENCES `class_going_on` (`class_going_on_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_slot`
--

LOCK TABLES `time_slot` WRITE;
/*!40000 ALTER TABLE `time_slot` DISABLE KEYS */;
INSERT INTO `time_slot` VALUES (1,'monday','1',26),(2,'monday','2',29),(4,'monday','3',32),(5,'tuesday','3',32),(6,'wednesday','3',32),(7,'wednesday','2',29),(8,'wednesday','1',26),(9,'tuesday','2',29),(10,'tuesday','3',32),(11,'friday','4',26);
/*!40000 ALTER TABLE `time_slot` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-22  9:37:29
