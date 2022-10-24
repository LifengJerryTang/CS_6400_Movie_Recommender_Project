-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: travel_reservation_service
-- ------------------------------------------------------
-- Server version	8.0.20

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `Email` varchar(50) NOT NULL,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Pass` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES ('aray@tiktok.com','Addison','Ray','password17'),('arthurread@gmail.com','Arthur','Read','password4'),('asmith@travelagency.com','Aviva','Smith','password2'),('boblee15@gmail.com','Bob','Lee','password25'),('bshelton@gmail.com','Blake','Shelton','password19'),('cbing10@gmail.com','Chandler','Bing','password13'),('cdemilio@tiktok.com','Charlie','Demilio','password18'),('ellie2@gmail.com','Ellie','Johnson','password10'),('gburdell3@gmail.com','George','Burdell','password6'),('hwmit@gmail.com','Howard','Wolowitz','password14'),('johnthomas@gmail.com','John','Thomas','password24'),('jseinfeld@gmail.com','Jerry','Seinfeld','password22'),('jwayne@gmail.com','John','Wayne','password5'),('lbryan@gmail.com','Luke','Bryan','password20'),('lebron6@gmail.com','Lebron','James','password8'),('maddiesmith@gmail.com','Madison','Smith','password23'),('mgeller5@gmail.com','Monica','Geller','password12'),('mj23@gmail.com','Michael','Jordan','password7'),('mmoss1@travelagency.com','Mark','Moss','password1'),('mscott22@gmail.com','Michael','Scott','password3'),('msmith5@gmail.com','Michael','Smith','password9'),('scooper3@gmail.com','Sheldon','Cooper','password11'),('swilson@gmail.com','Samantha','Wilson','password16'),('tswift@gmail.com','Taylor','Swift','password21');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `Email` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`),
  CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `accounts` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('asmith@travelagency.com'),('mmoss1@travelagency.com');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airline`
--

DROP TABLE IF EXISTS `airline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airline` (
  `Airline_Name` varchar(50) NOT NULL,
  `Rating` decimal(2,1) NOT NULL,
  PRIMARY KEY (`Airline_Name`),
  CONSTRAINT `airline_chk_1` CHECK (((`Rating` >= 1) and (`Rating` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airline`
--

LOCK TABLES `airline` WRITE;
/*!40000 ALTER TABLE `airline` DISABLE KEYS */;
INSERT INTO `airline` VALUES ('American Airlines',4.6),('Delta Airlines',4.7),('Interjet',3.7),('JetBlue Airways',3.6),('Southwest Airlines',4.4),('Spirit Airlines',3.3),('United Airlines',4.2),('WestJet',3.9);
/*!40000 ALTER TABLE `airline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airport` (
  `Airport_Id` char(3) NOT NULL,
  `Airport_Name` varchar(50) NOT NULL,
  `Time_Zone` char(3) NOT NULL,
  `Street` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `State` char(2) NOT NULL,
  `Zip` char(5) NOT NULL,
  PRIMARY KEY (`Airport_Id`),
  UNIQUE KEY `Airport_Name` (`Airport_Name`),
  UNIQUE KEY `Street` (`Street`,`City`,`State`,`Zip`),
  CONSTRAINT `airport_chk_1` CHECK ((length(`Airport_Id`) = 3)),
  CONSTRAINT `airport_chk_2` CHECK ((length(`Time_Zone`) = 3)),
  CONSTRAINT `airport_chk_3` CHECK ((length(`State`) = 2)),
  CONSTRAINT `airport_chk_4` CHECK ((length(`Zip`) = 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES ('ATL','Atlanta Hartsfield Jackson Airport','EST','6000 N Terminal Pkwy','Atlanta','GA','30320'),('DFW','Dallas International Airport','CST','2400 Aviation DR','Dallas','TX','75261'),('JFK','John F Kennedy International Airport','EST','455 Airport Ave','Queens','NY','11430'),('LAX','Lost Angeles International Airport','PST','1 World Way','Los Angeles','CA','90045'),('LGA','Laguardia Airport','EST','790 Airport St','Queens','NY','11371'),('MIA','Miami International Airport','EST','2100 NW 42nd Ave','Miami','FL','33126'),('ORD','O\'Hare International Airport','CST','10000 W O\'Hare Ave','Chicago','IL','60666'),('SJC','Norman Y. Mineta San Jose International Airport','PST','1702 Airport Blvd','San Jose','CA','95110');
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `amenity`
--

DROP TABLE IF EXISTS `amenity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenity` (
  `Property_Name` varchar(50) NOT NULL,
  `Property_Owner` varchar(50) NOT NULL,
  `Amenity_Name` varchar(50) NOT NULL,
  PRIMARY KEY (`Property_Name`,`Property_Owner`,`Amenity_Name`),
  CONSTRAINT `amenity_ibfk_1` FOREIGN KEY (`Property_Name`, `Property_Owner`) REFERENCES `property` (`Property_Name`, `Owner_Email`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenity`
--

LOCK TABLES `amenity` WRITE;
/*!40000 ALTER TABLE `amenity` DISABLE KEYS */;
INSERT INTO `amenity` VALUES ('Atlanta Great Property','scooper3@gmail.com','A/C & Heating'),('Atlanta Great Property','scooper3@gmail.com','Pets allowed'),('Atlanta Great Property','scooper3@gmail.com','Washer and Dryer'),('Atlanta Great Property','scooper3@gmail.com','Wifi & TV'),('Beautiful Beach Property','msmith5@gmail.com','A/C & Heating'),('Beautiful Beach Property','msmith5@gmail.com','Washer and Dryer'),('Beautiful Beach Property','msmith5@gmail.com','Wifi & TV'),('Beautiful San Jose Mansion','arthurread@gmail.com','A/C & Heating'),('Beautiful San Jose Mansion','arthurread@gmail.com','Full Kitchen'),('Beautiful San Jose Mansion','arthurread@gmail.com','Pets allowed'),('Beautiful San Jose Mansion','arthurread@gmail.com','Washer and Dryer'),('Beautiful San Jose Mansion','arthurread@gmail.com','Wifi & TV'),('Chicago Blackhawks House','hwmit@gmail.com','A/C & Heating'),('Chicago Blackhawks House','hwmit@gmail.com','Full Kitchen'),('Chicago Blackhawks House','hwmit@gmail.com','Washer and Dryer'),('Chicago Blackhawks House','hwmit@gmail.com','Wifi & TV'),('Chicago Romantic Getaway','mj23@gmail.com','A/C & Heating'),('Chicago Romantic Getaway','mj23@gmail.com','Wifi & TV'),('Family Beach House','ellie2@gmail.com','A/C & Heating'),('Family Beach House','ellie2@gmail.com','Full Kitchen'),('Family Beach House','ellie2@gmail.com','Pets allowed'),('Family Beach House','ellie2@gmail.com','Washer and Dryer'),('Family Beach House','ellie2@gmail.com','Wifi & TV'),('House near Georgia Tech','gburdell3@gmail.com','Full Kitchen'),('House near Georgia Tech','gburdell3@gmail.com','Washer and Dryer'),('House near Georgia Tech','gburdell3@gmail.com','Wifi & TV'),('LA Kings House','arthurread@gmail.com','A/C & Heating'),('LA Kings House','arthurread@gmail.com','Full Kitchen'),('LA Kings House','arthurread@gmail.com','Washer and Dryer'),('LA Kings House','arthurread@gmail.com','Wifi & TV'),('LA Lakers Property','lebron6@gmail.com','A/C & Heating'),('LA Lakers Property','lebron6@gmail.com','Full Kitchen'),('LA Lakers Property','lebron6@gmail.com','Washer and Dryer'),('LA Lakers Property','lebron6@gmail.com','Wifi & TV'),('Los Angeles Property','arthurread@gmail.com','A/C & Heating'),('Los Angeles Property','arthurread@gmail.com','Pets allowed'),('Los Angeles Property','arthurread@gmail.com','Wifi & TV'),('New York City Property','cbing10@gmail.com','A/C & Heating'),('New York City Property','cbing10@gmail.com','Wifi & TV'),('Statue of Libery Property','mgeller5@gmail.com','A/C & Heating'),('Statue of Libery Property','mgeller5@gmail.com','Wifi & TV'),('Texas Longhorns House','mscott22@gmail.com','A/C & Heating'),('Texas Longhorns House','mscott22@gmail.com','Full Kitchen'),('Texas Longhorns House','mscott22@gmail.com','Pets allowed'),('Texas Longhorns House','mscott22@gmail.com','Washer and Dryer'),('Texas Longhorns House','mscott22@gmail.com','Wifi & TV'),('Texas Roadhouse','mscott22@gmail.com','A/C & Heating'),('Texas Roadhouse','mscott22@gmail.com','Pets allowed'),('Texas Roadhouse','mscott22@gmail.com','Washer and Dryer'),('Texas Roadhouse','mscott22@gmail.com','Wifi & TV');
/*!40000 ALTER TABLE `amenity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attraction`
--

DROP TABLE IF EXISTS `attraction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attraction` (
  `Airport` char(3) NOT NULL,
  `Attraction_Name` varchar(50) NOT NULL,
  PRIMARY KEY (`Airport`,`Attraction_Name`),
  CONSTRAINT `attraction_ibfk_1` FOREIGN KEY (`Airport`) REFERENCES `airport` (`Airport_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attraction`
--

LOCK TABLES `attraction` WRITE;
/*!40000 ALTER TABLE `attraction` DISABLE KEYS */;
INSERT INTO `attraction` VALUES ('ATL','The Coke Factory'),('ATL','The Georgia Aquarium'),('DFW','Texas Longhorns Stadium'),('DFW','The Original Texas Roadhouse'),('JFK','The Empire State Building'),('JFK','The Statue of Liberty'),('LAX','Los Angeles Kings Stadium'),('LAX','Lost Angeles Lakers Stadium'),('LGA','The Empire State Building'),('LGA','The Statue of Liberty'),('MIA','Crandon Park Beach'),('MIA','Miami Heat Basketball Stadium'),('ORD','Chicago Blackhawks Stadium'),('ORD','Chicago Bulls Stadium'),('SJC','San Jose Earthquakes Soccer Team'),('SJC','Winchester Mystery House');
/*!40000 ALTER TABLE `attraction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `Customer` varchar(50) NOT NULL,
  `Flight_Num` char(5) NOT NULL,
  `Airline_Name` varchar(50) NOT NULL,
  `Num_Seats` int NOT NULL,
  `Was_Cancelled` tinyint(1) NOT NULL,
  PRIMARY KEY (`Customer`,`Flight_Num`,`Airline_Name`),
  KEY `Flight_Num` (`Flight_Num`,`Airline_Name`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`Customer`) REFERENCES `customer` (`Email`),
  CONSTRAINT `book_ibfk_2` FOREIGN KEY (`Flight_Num`, `Airline_Name`) REFERENCES `flight` (`Flight_Num`, `Airline_Name`),
  CONSTRAINT `book_chk_1` CHECK ((`Num_Seats` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES ('aray@tiktok.com','1','Delta Airlines',2,0),('bshelton@gmail.com','4','United Airlines',4,0),('bshelton@gmail.com','5','JetBlue Airways',4,1),('cbing10@gmail.com','2','Southwest Airlines',2,0),('hwmit@gmail.com','2','Southwest Airlines',5,1),('jseinfeld@gmail.com','7','WestJet',4,1),('lbryan@gmail.com','7','WestJet',2,0),('maddiesmith@gmail.com','8','Interjet',2,0),('swilson@gmail.com','5','JetBlue Airways',3,0),('tswift@gmail.com','7','WestJet',2,0);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `Email` varchar(50) NOT NULL,
  `Phone_Number` char(12) NOT NULL,
  PRIMARY KEY (`Email`),
  UNIQUE KEY `Phone_Number` (`Phone_Number`),
  CONSTRAINT `clients_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `accounts` (`Email`),
  CONSTRAINT `clients_chk_1` CHECK ((length(`Phone_Number`) = 12))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES ('boblee15@gmail.com','404-678-5555'),('johnthomas@gmail.com','404-770-5555'),('mscott22@gmail.com','555-123-4567'),('arthurread@gmail.com','555-234-5678'),('jwayne@gmail.com','555-345-6789'),('gburdell3@gmail.com','555-456-7890'),('mj23@gmail.com','555-567-8901'),('lebron6@gmail.com','555-678-9012'),('msmith5@gmail.com','555-789-0123'),('ellie2@gmail.com','555-890-1234'),('scooper3@gmail.com','678-123-4567'),('mgeller5@gmail.com','678-234-5678'),('cbing10@gmail.com','678-345-6789'),('hwmit@gmail.com','678-456-7890'),('swilson@gmail.com','770-123-4567'),('aray@tiktok.com','770-234-5678'),('cdemilio@tiktok.com','770-345-6789'),('bshelton@gmail.com','770-456-7890'),('lbryan@gmail.com','770-567-8901'),('tswift@gmail.com','770-678-9012'),('jseinfeld@gmail.com','770-789-0123'),('maddiesmith@gmail.com','770-890-1234');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `Email` varchar(50) NOT NULL,
  `CcNumber` varchar(19) NOT NULL,
  `Cvv` char(3) NOT NULL,
  `Exp_Date` date NOT NULL,
  `Location` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`),
  UNIQUE KEY `CcNumber` (`CcNumber`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `clients` (`Email`),
  CONSTRAINT `customer_chk_1` CHECK ((length(`CcNumber`) = 19)),
  CONSTRAINT `customer_chk_2` CHECK ((length(`Cvv`) = 3))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('aray@tiktok.com','3110 2669 7949 5605','744','2022-08-01',''),('boblee15@gmail.com','7907 3513 7161 4248','858','2025-11-01',''),('bshelton@gmail.com','9276 7639 7883 4273','862','2023-09-01',''),('cbing10@gmail.com','8387 9523 9827 9291','201','2023-02-01',''),('cdemilio@tiktok.com','2272 3555 4078 4744','606','2025-02-01',''),('hwmit@gmail.com','6558 8596 9852 5299','102','2023-04-01',''),('johnthomas@gmail.com','7580 3274 3724 5356','269','2025-10-01',''),('jseinfeld@gmail.com','3616 8977 1296 3372','295','2022-06-01',''),('lbryan@gmail.com','4652 3726 8864 3798','258','2023-05-01',''),('maddiesmith@gmail.com','9954 5698 6355 6952','794','2022-07-01',''),('mgeller5@gmail.com','2328 5670 4310 1965','644','2024-03-01',''),('scooper3@gmail.com','6518 5559 7446 1663','551','2024-02-01',''),('swilson@gmail.com','9383 3212 4198 1836','455','2022-08-01',''),('tswift@gmail.com','5478 8420 4436 7471','857','2024-12-01','');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers_rate_owners`
--

DROP TABLE IF EXISTS `customers_rate_owners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_rate_owners` (
  `Customer` varchar(50) NOT NULL,
  `Owner_Email` varchar(50) NOT NULL,
  `Score` int NOT NULL,
  PRIMARY KEY (`Customer`,`Owner_Email`),
  KEY `Owner_Email` (`Owner_Email`),
  CONSTRAINT `customers_rate_owners_ibfk_1` FOREIGN KEY (`Customer`) REFERENCES `customer` (`Email`),
  CONSTRAINT `customers_rate_owners_ibfk_2` FOREIGN KEY (`Owner_Email`) REFERENCES `owners` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `customers_rate_owners_chk_1` CHECK (((`Score` >= 1) and (`Score` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_rate_owners`
--

LOCK TABLES `customers_rate_owners` WRITE;
/*!40000 ALTER TABLE `customers_rate_owners` DISABLE KEYS */;
INSERT INTO `customers_rate_owners` VALUES ('aray@tiktok.com','cbing10@gmail.com',5),('bshelton@gmail.com','mgeller5@gmail.com',3),('jseinfeld@gmail.com','lebron6@gmail.com',1),('lbryan@gmail.com','arthurread@gmail.com',4),('maddiesmith@gmail.com','hwmit@gmail.com',2),('swilson@gmail.com','gburdell3@gmail.com',5),('tswift@gmail.com','arthurread@gmail.com',4);
/*!40000 ALTER TABLE `customers_rate_owners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight` (
  `Flight_Num` char(5) NOT NULL,
  `Airline_Name` varchar(50) NOT NULL,
  `From_Airport` char(3) NOT NULL,
  `To_Airport` char(3) NOT NULL,
  `Departure_Time` time NOT NULL,
  `Arrival_Time` time NOT NULL,
  `Flight_Date` date NOT NULL,
  `Cost` decimal(6,2) NOT NULL,
  `Capacity` int NOT NULL,
  PRIMARY KEY (`Flight_Num`,`Airline_Name`),
  KEY `Airline_Name` (`Airline_Name`),
  KEY `From_Airport` (`From_Airport`),
  KEY `To_Airport` (`To_Airport`),
  CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`Airline_Name`) REFERENCES `airline` (`Airline_Name`),
  CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`From_Airport`) REFERENCES `airport` (`Airport_Id`),
  CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`To_Airport`) REFERENCES `airport` (`Airport_Id`),
  CONSTRAINT `flight_chk_1` CHECK ((`Cost` >= 0)),
  CONSTRAINT `flight_chk_2` CHECK ((`Capacity` > 0)),
  CONSTRAINT `flight_chk_3` CHECK ((`From_Airport` <> `To_Airport`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight`
--

LOCK TABLES `flight` WRITE;
/*!40000 ALTER TABLE `flight` DISABLE KEYS */;
INSERT INTO `flight` VALUES ('1','Delta Airlines','ATL','JFK','10:00:00','12:00:00','2022-10-18',400.00,150),('10','Delta Airlines','LAX','ATL','09:15:00','18:15:00','2022-10-20',700.00,110),('11','Southwest Airlines','LAX','ORD','12:07:00','19:07:00','2022-10-20',600.00,95),('12','United Airlines','MIA','ATL','15:35:00','17:35:00','2022-10-20',275.00,115),('2','Southwest Airlines','ORD','MIA','10:30:00','14:30:00','2022-10-18',350.00,125),('3','American Airlines','MIA','DFW','13:00:00','16:00:00','2022-10-18',350.00,125),('4','United Airlines','ATL','LGA','16:30:00','18:30:00','2022-10-18',400.00,100),('5','JetBlue Airways','LGA','ATL','11:00:00','13:00:00','2022-10-19',400.00,130),('6','Spirit Airlines','SJC','ATL','12:30:00','21:30:00','2022-10-19',650.00,140),('7','WestJet','LGA','SJC','13:00:00','16:00:00','2022-10-19',700.00,100),('8','Interjet','MIA','ORD','19:30:00','21:30:00','2022-10-19',350.00,125),('9','Delta Airlines','JFK','ATL','08:00:00','10:00:00','2022-10-20',375.00,150);
/*!40000 ALTER TABLE `flight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `is_close_to`
--

DROP TABLE IF EXISTS `is_close_to`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `is_close_to` (
  `Property_Name` varchar(50) NOT NULL,
  `Owner_Email` varchar(50) NOT NULL,
  `Airport` char(3) NOT NULL,
  `Distance` int NOT NULL,
  PRIMARY KEY (`Property_Name`,`Owner_Email`,`Airport`),
  KEY `Airport` (`Airport`),
  CONSTRAINT `is_close_to_ibfk_1` FOREIGN KEY (`Property_Name`, `Owner_Email`) REFERENCES `property` (`Property_Name`, `Owner_Email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `is_close_to_ibfk_2` FOREIGN KEY (`Airport`) REFERENCES `airport` (`Airport_Id`),
  CONSTRAINT `is_close_to_chk_1` CHECK ((`Distance` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `is_close_to`
--

LOCK TABLES `is_close_to` WRITE;
/*!40000 ALTER TABLE `is_close_to` DISABLE KEYS */;
INSERT INTO `is_close_to` VALUES ('Atlanta Great Property','scooper3@gmail.com','ATL',12),('Beautiful Beach Property','msmith5@gmail.com','MIA',21),('Beautiful San Jose Mansion','arthurread@gmail.com','LAX',30),('Beautiful San Jose Mansion','arthurread@gmail.com','SJC',8),('Chicago Blackhawks House','hwmit@gmail.com','ORD',11),('Chicago Romantic Getaway','mj23@gmail.com','ORD',13),('Family Beach House','ellie2@gmail.com','MIA',19),('House near Georgia Tech','gburdell3@gmail.com','ATL',7),('LA Kings House','arthurread@gmail.com','LAX',12),('LA Lakers Property','lebron6@gmail.com','LAX',6),('Los Angeles Property','arthurread@gmail.com','LAX',9),('New York City Property','cbing10@gmail.com','JFK',10),('New York City Property','cbing10@gmail.com','LGA',25),('Statue of Libery Property','mgeller5@gmail.com','JFK',8),('Statue of Libery Property','mgeller5@gmail.com','LGA',19),('Texas Longhorns House','mscott22@gmail.com','DFW',17),('Texas Roadhouse','mscott22@gmail.com','DFW',8);
/*!40000 ALTER TABLE `is_close_to` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owners`
--

DROP TABLE IF EXISTS `owners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owners` (
  `Email` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`),
  CONSTRAINT `owners_ibfk_1` FOREIGN KEY (`Email`) REFERENCES `clients` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owners`
--

LOCK TABLES `owners` WRITE;
/*!40000 ALTER TABLE `owners` DISABLE KEYS */;
INSERT INTO `owners` VALUES ('arthurread@gmail.com'),('cbing10@gmail.com'),('ellie2@gmail.com'),('gburdell3@gmail.com'),('hwmit@gmail.com'),('jwayne@gmail.com'),('lebron6@gmail.com'),('mgeller5@gmail.com'),('mj23@gmail.com'),('mscott22@gmail.com'),('msmith5@gmail.com'),('scooper3@gmail.com');
/*!40000 ALTER TABLE `owners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owners_rate_customers`
--

DROP TABLE IF EXISTS `owners_rate_customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owners_rate_customers` (
  `Owner_Email` varchar(50) NOT NULL,
  `Customer` varchar(50) NOT NULL,
  `Score` int NOT NULL,
  PRIMARY KEY (`Owner_Email`,`Customer`),
  KEY `Customer` (`Customer`),
  CONSTRAINT `owners_rate_customers_ibfk_1` FOREIGN KEY (`Owner_Email`) REFERENCES `owners` (`Email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `owners_rate_customers_ibfk_2` FOREIGN KEY (`Customer`) REFERENCES `customer` (`Email`),
  CONSTRAINT `owners_rate_customers_chk_1` CHECK (((`Score` >= 1) and (`Score` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owners_rate_customers`
--

LOCK TABLES `owners_rate_customers` WRITE;
/*!40000 ALTER TABLE `owners_rate_customers` DISABLE KEYS */;
INSERT INTO `owners_rate_customers` VALUES ('arthurread@gmail.com','lbryan@gmail.com',4),('arthurread@gmail.com','tswift@gmail.com',4),('cbing10@gmail.com','aray@tiktok.com',5),('gburdell3@gmail.com','swilson@gmail.com',5),('hwmit@gmail.com','maddiesmith@gmail.com',2),('lebron6@gmail.com','jseinfeld@gmail.com',1),('mgeller5@gmail.com','bshelton@gmail.com',3);
/*!40000 ALTER TABLE `owners_rate_customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `Property_Name` varchar(50) NOT NULL,
  `Owner_Email` varchar(50) NOT NULL,
  `Descr` varchar(500) NOT NULL,
  `Capacity` int NOT NULL,
  `Cost` decimal(6,2) NOT NULL,
  `Street` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `State` char(2) NOT NULL,
  `Zip` char(5) NOT NULL,
  PRIMARY KEY (`Property_Name`,`Owner_Email`),
  UNIQUE KEY `Street` (`Street`,`City`,`State`,`Zip`),
  KEY `Owner_Email` (`Owner_Email`),
  CONSTRAINT `property_ibfk_1` FOREIGN KEY (`Owner_Email`) REFERENCES `owners` (`Email`),
  CONSTRAINT `property_chk_1` CHECK ((`Capacity` > 0)),
  CONSTRAINT `property_chk_2` CHECK ((`Cost` >= 0)),
  CONSTRAINT `property_chk_3` CHECK ((length(`State`) = 2)),
  CONSTRAINT `property_chk_4` CHECK ((length(`Zip`) = 5))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
INSERT INTO `property` VALUES ('Atlanta Great Property','scooper3@gmail.com','This is right in the middle of Atlanta near many attractions!',4,600.00,'2nd St','ATL','GA','30008'),('Beautiful Beach Property','msmith5@gmail.com','You can walk out of the house and be on the beach!',2,975.00,'456 Beach Ave','Miami','FL','33101'),('Beautiful San Jose Mansion','arthurread@gmail.com','Huge house that can sleep 12 people. Totally worth it!',12,900.00,'Golden Bridge Pkwt','San Jose','CA','90001'),('Chicago Blackhawks House','hwmit@gmail.com','This is a great property!',3,775.00,'Blackhawks St','Chicago','IL','60176'),('Chicago Romantic Getaway','mj23@gmail.com','This is a great property!',2,1050.00,'23rd Main St','Chicago','IL','60176'),('Family Beach House','ellie2@gmail.com','You can literally walk onto the beach and see it from the patio!',6,850.00,'1132 Beach Ave','Miami','FL','33101'),('House near Georgia Tech','gburdell3@gmail.com','Super close to bobby dodde stadium!',3,275.00,'North Ave','ATL','GA','30008'),('LA Kings House','arthurread@gmail.com','This house is super close to the LA kinds stadium!',4,750.00,'Kings St','La','CA','90011'),('LA Lakers Property','lebron6@gmail.com','This house is right near the LA lakers stadium. You might even meet Lebron James!',4,850.00,'Lebron Ave','LA','CA','90011'),('Los Angeles Property','arthurread@gmail.com','',3,700.00,'10th St','LA','CA','90008'),('New York City Property','cbing10@gmail.com','A view of the whole city. Great property!',2,750.00,'123 Main St','NYC','NY','10008'),('Statue of Libery Property','mgeller5@gmail.com','You can see the statue of liberty from the porch',5,1000.00,'1st St','NYC','NY','10009'),('Texas Longhorns House','mscott22@gmail.com','You can walk to the longhorns stadium from here!',10,600.00,'1125 Longhorns Way','Dallas','TX','75001'),('Texas Roadhouse','mscott22@gmail.com','This property is right in the center of Dallas, Texas!',3,450.00,'17th Street','Dallas','TX','75043');
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `query_1`
--

DROP TABLE IF EXISTS `query_1`;
/*!50001 DROP VIEW IF EXISTS `query_1`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_1` AS SELECT 
 1 AS `Email`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_10`
--

DROP TABLE IF EXISTS `query_10`;
/*!50001 DROP VIEW IF EXISTS `query_10`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_10` AS SELECT 
 1 AS `Airline_Name`,
 1 AS `Seats_Booked`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_2`
--

DROP TABLE IF EXISTS `query_2`;
/*!50001 DROP VIEW IF EXISTS `query_2`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_2` AS SELECT 
 1 AS `Property_Name`,
 1 AS `Email`,
 1 AS `CcNumber`,
 1 AS `Cvv`,
 1 AS `Exp_Date`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_3`
--

DROP TABLE IF EXISTS `query_3`;
/*!50001 DROP VIEW IF EXISTS `query_3`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_3` AS SELECT 
 1 AS `Owner_Email`,
 1 AS `Property_Name`,
 1 AS `Content`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_4`
--

DROP TABLE IF EXISTS `query_4`;
/*!50001 DROP VIEW IF EXISTS `query_4`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_4` AS SELECT 
 1 AS `To_Airport`,
 1 AS `AVG(Cost)`,
 1 AS `AVG(Capacity)`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_5`
--

DROP TABLE IF EXISTS `query_5`;
/*!50001 DROP VIEW IF EXISTS `query_5`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_5` AS SELECT 
 1 AS `Property_Name`,
 1 AS `Owner_Email`,
 1 AS `Airport`,
 1 AS `Distance`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_6`
--

DROP TABLE IF EXISTS `query_6`;
/*!50001 DROP VIEW IF EXISTS `query_6`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_6` AS SELECT 
 1 AS `Email`,
 1 AS `First_Name`,
 1 AS `Last_Name`,
 1 AS `Phone_Number`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_7`
--

DROP TABLE IF EXISTS `query_7`;
/*!50001 DROP VIEW IF EXISTS `query_7`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_7` AS SELECT 
 1 AS `Flight_Num`,
 1 AS `Airline_Name`,
 1 AS `From_Airport`,
 1 AS `To_Airport`,
 1 AS `Departure_Time`,
 1 AS `Arrival_Time`,
 1 AS `Flight_Date`,
 1 AS `Cost`,
 1 AS `Capacity`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_8`
--

DROP TABLE IF EXISTS `query_8`;
/*!50001 DROP VIEW IF EXISTS `query_8`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_8` AS SELECT 
 1 AS `Property_Name`,
 1 AS `Owner_Email`,
 1 AS `Amenities`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `query_9`
--

DROP TABLE IF EXISTS `query_9`;
/*!50001 DROP VIEW IF EXISTS `query_9`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `query_9` AS SELECT 
 1 AS `Email`,
 1 AS `CcNumber`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `reserve`
--

DROP TABLE IF EXISTS `reserve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserve` (
  `Property_Name` varchar(50) NOT NULL,
  `Owner_Email` varchar(50) NOT NULL,
  `Customer` varchar(50) NOT NULL,
  `Start_Date` date NOT NULL,
  `End_Date` date NOT NULL,
  `Num_Guests` int NOT NULL,
  `Was_Cancelled` tinyint(1) NOT NULL,
  PRIMARY KEY (`Property_Name`,`Owner_Email`,`Customer`),
  KEY `Customer` (`Customer`),
  CONSTRAINT `reserve_ibfk_1` FOREIGN KEY (`Property_Name`, `Owner_Email`) REFERENCES `property` (`Property_Name`, `Owner_Email`),
  CONSTRAINT `reserve_ibfk_2` FOREIGN KEY (`Customer`) REFERENCES `customer` (`Email`),
  CONSTRAINT `reserve_chk_1` CHECK ((`Num_Guests` > 0)),
  CONSTRAINT `reserve_chk_2` CHECK ((`End_Date` >= `Start_Date`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserve`
--

LOCK TABLES `reserve` WRITE;
/*!40000 ALTER TABLE `reserve` DISABLE KEYS */;
INSERT INTO `reserve` VALUES ('Beautiful Beach Property','msmith5@gmail.com','cbing10@gmail.com','2022-10-18','2022-10-25',2,0),('Beautiful San Jose Mansion','arthurread@gmail.com','tswift@gmail.com','2022-10-19','2022-10-22',10,0),('Chicago Blackhawks House','hwmit@gmail.com','maddiesmith@gmail.com','2022-10-19','2022-10-23',2,0),('Chicago Romantic Getaway','mj23@gmail.com','aray@tiktok.com','2022-11-01','2022-11-07',2,1),('Family Beach House','ellie2@gmail.com','hwmit@gmail.com','2022-10-18','2022-10-28',5,1),('House near Georgia Tech','gburdell3@gmail.com','swilson@gmail.com','2022-10-19','2022-10-25',3,0),('LA Lakers Property','lebron6@gmail.com','jseinfeld@gmail.com','2022-10-19','2022-10-24',4,0),('Los Angeles Property','arthurread@gmail.com','lbryan@gmail.com','2022-10-19','2022-10-25',2,0),('New York City Property','cbing10@gmail.com','aray@tiktok.com','2022-10-18','2022-10-23',2,0),('New York City Property','cbing10@gmail.com','cdemilio@tiktok.com','2022-10-24','2022-10-30',2,0),('New York City Property','cbing10@gmail.com','mgeller5@gmail.com','2022-11-02','2022-11-06',3,1),('Statue of Libery Property','mgeller5@gmail.com','bshelton@gmail.com','2022-10-18','2022-10-22',4,0);
/*!40000 ALTER TABLE `reserve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `Property_Name` varchar(50) NOT NULL,
  `Owner_Email` varchar(50) NOT NULL,
  `Customer` varchar(50) NOT NULL,
  `Content` varchar(500) DEFAULT NULL,
  `Score` int NOT NULL,
  PRIMARY KEY (`Property_Name`,`Owner_Email`,`Customer`),
  KEY `Customer` (`Customer`),
  CONSTRAINT `review_ibfk_1` FOREIGN KEY (`Property_Name`, `Owner_Email`) REFERENCES `property` (`Property_Name`, `Owner_Email`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `review_ibfk_2` FOREIGN KEY (`Customer`) REFERENCES `customer` (`Email`),
  CONSTRAINT `review_chk_1` CHECK (((`Score` >= 1) and (`Score` <= 5)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES ('Beautiful San Jose Mansion','arthurread@gmail.com','tswift@gmail.com','We had a great time, but the house wasn\'t fully cleaned when we arrived',3),('Chicago Blackhawks House','hwmit@gmail.com','maddiesmith@gmail.com','This was awesome! I met one player on the chicago blackhawks!',5),('House near Georgia Tech','gburdell3@gmail.com','swilson@gmail.com','This was so much fun. I went and saw the coke factory, the falcons play, GT play, and the Georgia aquarium. Great time! Would highly recommend!',5),('LA Lakers Property','lebron6@gmail.com','jseinfeld@gmail.com','I was disappointed that I did not meet lebron james',2),('Los Angeles Property','arthurread@gmail.com','lbryan@gmail.com','I had an excellent time!',4),('New York City Property','cbing10@gmail.com','aray@tiktok.com','This was the best 5 days ever! I saw so much of NYC!',5),('New York City Property','cbing10@gmail.com','cdemilio@tiktok.com','It was decent, but could have been better',4),('Statue of Libery Property','mgeller5@gmail.com','bshelton@gmail.com','This was truly an excellent experience. I really could see the Statue of Liberty from the property!',4);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `seats_booked`
--

DROP TABLE IF EXISTS `seats_booked`;
/*!50001 DROP VIEW IF EXISTS `seats_booked`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `seats_booked` AS SELECT 
 1 AS `Airline_Name`,
 1 AS `Seats_Booked`,
 1 AS `Flight_Date`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `query_1`
--

/*!50001 DROP VIEW IF EXISTS `query_1`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_1` AS select `clients`.`Email` AS `Email` from `clients` where ((`clients`.`Phone_Number` like '555%') or (`clients`.`Phone_Number` like '404%')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_10`
--

/*!50001 DROP VIEW IF EXISTS `query_10`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_10` AS select `seats_booked`.`Airline_Name` AS `Airline_Name`,`seats_booked`.`Seats_Booked` AS `Seats_Booked` from `seats_booked` where (`seats_booked`.`Flight_Date` = '2022-10-18') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_2`
--

/*!50001 DROP VIEW IF EXISTS `query_2`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_2` AS select `reserve`.`Property_Name` AS `Property_Name`,`customer`.`Email` AS `Email`,`customer`.`CcNumber` AS `CcNumber`,`customer`.`Cvv` AS `Cvv`,`customer`.`Exp_Date` AS `Exp_Date` from (`customer` join `reserve` on((`customer`.`Email` = `reserve`.`Customer`))) where ((`reserve`.`Start_Date` between '2022-10-15' and '2022-10-20') and (`reserve`.`End_Date` between '2022-10-21' and '2022-10-30')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_3`
--

/*!50001 DROP VIEW IF EXISTS `query_3`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_3` AS select `review`.`Owner_Email` AS `Owner_Email`,`review`.`Property_Name` AS `Property_Name`,`review`.`Content` AS `Content` from `review` where ((length(`review`.`Content`) > 25) and ((`review`.`Content` like '%great%') or (`review`.`Content` like '%excellent%'))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_4`
--

/*!50001 DROP VIEW IF EXISTS `query_4`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_4` AS select `flight`.`To_Airport` AS `To_Airport`,avg(`flight`.`Cost`) AS `AVG(Cost)`,avg(`flight`.`Capacity`) AS `AVG(Capacity)` from `flight` group by `flight`.`To_Airport` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_5`
--

/*!50001 DROP VIEW IF EXISTS `query_5`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_5` AS select `b`.`Property_Name` AS `Property_Name`,`b`.`Owner_Email` AS `Owner_Email`,`b`.`Airport` AS `Airport`,`b`.`Distance` AS `Distance` from ((select `is_close_to`.`Airport` AS `Airport`,min(`is_close_to`.`Distance`) AS `min_dist` from `is_close_to` group by `is_close_to`.`Airport`) `a` join `is_close_to` `b` on((`b`.`Distance` = `a`.`min_dist`))) group by `b`.`Property_Name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_6`
--

/*!50001 DROP VIEW IF EXISTS `query_6`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_6` AS select `accounts`.`Email` AS `Email`,`accounts`.`First_Name` AS `First_Name`,`accounts`.`Last_Name` AS `Last_Name`,`clients`.`Phone_Number` AS `Phone_Number` from (`accounts` join `clients` on((`accounts`.`Email` = `clients`.`Email`))) order by `accounts`.`Last_Name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_7`
--

/*!50001 DROP VIEW IF EXISTS `query_7`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_7` AS select `flight`.`Flight_Num` AS `Flight_Num`,`flight`.`Airline_Name` AS `Airline_Name`,`flight`.`From_Airport` AS `From_Airport`,`flight`.`To_Airport` AS `To_Airport`,`flight`.`Departure_Time` AS `Departure_Time`,`flight`.`Arrival_Time` AS `Arrival_Time`,`flight`.`Flight_Date` AS `Flight_Date`,`flight`.`Cost` AS `Cost`,`flight`.`Capacity` AS `Capacity` from `flight` order by `flight`.`Cost`,`flight`.`Flight_Date` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_8`
--

/*!50001 DROP VIEW IF EXISTS `query_8`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_8` AS select `property`.`Property_Name` AS `Property_Name`,`property`.`Owner_Email` AS `Owner_Email`,group_concat(`amenity`.`Amenity_Name` separator ',') AS `Amenities` from (`property` join `amenity` on(((`property`.`Property_Name` = `amenity`.`Property_Name`) and (`property`.`Owner_Email` = `amenity`.`Property_Owner`)))) group by `property`.`Property_Name`,`property`.`Owner_Email` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `query_9`
--

/*!50001 DROP VIEW IF EXISTS `query_9`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `query_9` AS select `customer`.`Email` AS `Email`,`customer`.`CcNumber` AS `CcNumber` from (`customer` join `book` on((`customer`.`Email` = `book`.`Customer`))) where (`book`.`Was_Cancelled` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `seats_booked`
--

/*!50001 DROP VIEW IF EXISTS `seats_booked`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `seats_booked` AS select `flight`.`Airline_Name` AS `Airline_Name`,sum(`book`.`Num_Seats`) AS `Seats_Booked`,`flight`.`Flight_Date` AS `Flight_Date` from (`flight` join `book` on(((`flight`.`Flight_Num` = `book`.`Flight_Num`) and (`flight`.`Airline_Name` = `book`.`Airline_Name`)))) where (`book`.`Was_Cancelled` = 0) group by `flight`.`Airline_Name` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-23 23:14:57
