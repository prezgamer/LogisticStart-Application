-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `courier`
--

DROP TABLE IF EXISTS `courier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courier` (
  `Customer_Account_ID` int(11) NOT NULL,
  `Parcel_Parcel_ID` int(11) NOT NULL,
  `Delivery_Status` varchar(45) NOT NULL,
  `Sender_Name` varchar(45) NOT NULL,
  `Sender_Address` varchar(255) NOT NULL,
  `Receiver_Name` varchar(45) NOT NULL,
  `Receiver_Address` varchar(255) NOT NULL,
  PRIMARY KEY (`Customer_Account_ID`,`Parcel_Parcel_ID`),
  KEY `fk_Customer_has_Parcel_Parcel1` (`Parcel_Parcel_ID`),
  CONSTRAINT `fk_Customer_has_Parcel_Customer` FOREIGN KEY (`Customer_Account_ID`) REFERENCES `customer` (`Account_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Customer_has_Parcel_Parcel1` FOREIGN KEY (`Parcel_Parcel_ID`) REFERENCES `parcel` (`Parcel_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courier`
--

LOCK TABLES `courier` WRITE;
/*!40000 ALTER TABLE `courier` DISABLE KEYS */;
INSERT INTO `courier` VALUES (1,50000002,'In Transit','John Doe','789 Oak Street, Springfield, IL','Jane Smith','101 Pine Street, Springfield, IL'),(3,50000001,'Delivered','Alice Johnson','123 Maple Street, Springfield, IL','Bob Brown','456 Elm Street, Springfield, IL'),(5,50000003,'Pending','Charlie Davis','202 Birch Street, Springfield, IL','Frank Green','303 Cedar Street, Springfield, IL'),(6,50000004,'Delivered','Diana Evans','404 Walnut Street, Springfield, IL','Grace Hall','505 Ash Street, Springfield, IL'),(9,50000005,'In Transit','Henry White','606 Beech Street, Springfield, IL','Ivy King','707 Chestnut Street, Springfield, IL');
/*!40000 ALTER TABLE `courier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `Account_ID` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Contact_No` int(11) NOT NULL,
  PRIMARY KEY (`Account_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'John Doe','john.doe@example.com',1234567890),(2,'Jane Smith','jane.smith@example.com',2147483647),(3,'Alice Johnson','alice.johnson@example.com',2147483647),(4,'Bob Brown','bob.brown@example.com',2147483647),(5,'Charlie Davis','charlie.davis@example.com',2147483647),(6,'Diana Evans','diana.evans@example.com',2147483647),(7,'Frank Green','frank.green@example.com',2147483647),(8,'Grace Hall','grace.hall@example.com',2147483647),(9,'Henry White','henry.white@example.com',2147483647),(10,'Ivy King','ivy.king@example.com',1234567891);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parcel`
--

DROP TABLE IF EXISTS `parcel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parcel` (
  `Parcel_ID` int(11) NOT NULL,
  `Content_Type` varchar(45) NOT NULL,
  `Content_Description` varchar(100) NOT NULL,
  PRIMARY KEY (`Parcel_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parcel`
--

LOCK TABLES `parcel` WRITE;
/*!40000 ALTER TABLE `parcel` DISABLE KEYS */;
INSERT INTO `parcel` VALUES (50000001,'Electronics','Smartphone with accessories'),(50000002,'Books','Fiction novel collection'),(50000003,'Clothing','Men’s winter jacket'),(50000004,'Toys','Lego building set'),(50000005,'Groceries','Organic vegetables and fruits');
/*!40000 ALTER TABLE `parcel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-21 20:45:10
