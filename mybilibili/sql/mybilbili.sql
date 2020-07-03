-- MySQL dump 10.13  Distrib 8.0.19, for macos10.15 (x86_64)
--
-- Host: localhost    Database: mybilibili
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bilibili_user_info`
--

DROP TABLE IF EXISTS `bilibili_user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bilibili_user_info` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `mid` int unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  `sex` varchar(45) NOT NULL,
  `face` varchar(200) NOT NULL,
  `sign` varchar(300) NOT NULL,
  `urank` varchar(45) NOT NULL,
  `level` int unsigned NOT NULL,
  `birthday` varchar(45) NOT NULL,
  `fans_badge` varchar(45) NOT NULL,
  `official_role` int unsigned NOT NULL,
  `official_title` varchar(200) NOT NULL,
  `official_desc` varchar(100) NOT NULL,
  `official_type` varchar(45) NOT NULL,
  `vip_type` varchar(45) NOT NULL,
  `vip_status` varchar(45) NOT NULL,
  `tags` varchar(200) NOT NULL,
  `following` int unsigned NOT NULL,
  `fans` int unsigned NOT NULL,
  `archiveview` int unsigned NOT NULL,
  `article` int unsigned NOT NULL,
  `likes` int unsigned NOT NULL,
  `video` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mid` (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bilibili_user_info`
--

LOCK TABLES `bilibili_user_info` WRITE;
/*!40000 ALTER TABLE `bilibili_user_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `bilibili_user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-10  2:05:37
