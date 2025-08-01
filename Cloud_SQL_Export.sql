-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: flask_auth
-- ------------------------------------------------------
-- Server version	8.0.41-google

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
-- Current Database: `flask_auth`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `flask_auth` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `flask_auth`;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `bio` text,
  `photo` varchar(255) DEFAULT NULL,
  `skills` text,
  `aspiration` text,
  `cv_file` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Prashob Preman','vp.prashob@gmail.com','$2b$12$yfCWDUlMFeCIBppNSno5i.8iMTUSA1N64kqjy8chKbJa5NwTXXGM6','Pullur','Ich bin Prashob','184-01-28-2022_04.jpg','Python,Flask,Django,Pyspark','Fullstack developer','Prashob_Preman.pdf'),(2,'Ram Rajeshwaran','destintouch@gmail.com','$2b$12$5zbiORG/8EXEBfqplpasxO0faGfALUpqCM03kwXRTsVYALh1eOUua',NULL,NULL,NULL,NULL,NULL,NULL),(4,'Vicky','vicksp770@gmail.com','$2b$12$G4RFLGssJc9wa8DwGIsLpuhWAntgGpSxbDpvvJpm2fqRMMbMJtx5y','Warsaw Poland','','1000079685.heic','Wintel Administrator, Linux Administrator','Cloud Administrator',NULL),(5,'Vaibhav ','vaibhavbharti1990@gmail.com','$2b$12$yXY0dGxoge.aQ1337cbuiucYuvHalFY.vXswcNz0kZa..qi.XV5Ay',NULL,NULL,NULL,NULL,NULL,NULL),(6,'Souvik Bhattacharjee','souvikbhattacharjee2022@gmail.com','$2b$12$2UfDKlNi5V.xbiGwizxEiuT80PmAUh6mVXKak99dxgMKSNRMdTqPa','Warsaw','','DSC08347.jpg','Linux, Jenkins, Git, Docker, Ansible','Devops Engineer','Souvik_Poland_CV.pdf');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-01  9:07:13
