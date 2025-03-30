/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - multisource
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

SET FOREIGN_KEY_CHECKS=0;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`multisource` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `multisource`;

/*Table structure for table `addoctors` */

DROP TABLE IF EXISTS `addoctors`;

CREATE TABLE `addoctors` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

 ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `addoctors` */

insert  into `addoctors`(`int`,`name`,`age`,`role`) values (1,'lh',22,'Cardiologist'),(2,'naresh@gmail.com',45,'eee'),(3,'lakshmi',54,'Fever');

/*Table structure for table `addrequesttodoctor` */

DROP TABLE IF EXISTS `addrequesttodoctor`;

CREATE TABLE `addrequesttodoctor` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int(100) DEFAULT NULL,
  `disease` varchar(100) DEFAULT NULL,
  `patientid` int(50) DEFAULT NULL,
  `doctorid` int(50) DEFAULT NULL,
  `appointmentdate` date DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `doctorname` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `addrequesttodoctor` */

insert  into `addrequesttodoctor`(`sno`,`name`,`age`,`disease`,`patientid`,`doctorid`,`appointmentdate`,`status`,`doctorname`) values (1,'Keerthana',22,'card',1,1,NULL,NULL,NULL),(2,'Keerthana',22,'Fever',1,5,'2022-08-11','accepted','lakshmi');

/*Table structure for table `adpatients` */

DROP TABLE IF EXISTS `adpatients`;

CREATE TABLE `adpatients` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int(100) DEFAULT NULL,
  `disease` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `adpatients` */

insert  into `adpatients`(`sno`,`name`,`age`,`disease`) values (1,'oo',12,'liui'),(2,'oo',12,'liui'),(3,'oo',34,'liui'),(4,'Keerthana',33,'Fever');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `age` int(50) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `cpwd` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `mobile` int(20) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `doctor` */

insert  into `doctor`(`sno`,`name`,`email`,`age`,`pwd`,`cpwd`,`gender`,`mobile`,`role`) values (1,'lh','naresh@gmail.com',22,'12','12','Male',2147483647,'Cardiologist'),(2,'l','naresh@gmail.com',90,'00','00','Male',2147483647,'Cardiologist'),(3,'ll','naresh@gmail.com',54,'44','44','Female',1524651,';.kl'),(4,'naresh@gmail.com','naresh@gmail.com',33,'1','1','Male',2147483647,'eee'),(5,'lakshmi','cse.takeoff@gmail.com',54,'123','123','Female',2147483647,'Fever');

/*Table structure for table `filesupload` */

DROP TABLE IF EXISTS `filesupload`;

CREATE TABLE `filesupload` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `files` longblob,
  `requeststofiles` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `filesupload` */

insert  into `filesupload`(`sno`,`files`,`requeststofiles`) values (1,'�z�Ki�i�E�Q�0G\'�`��!/��bG-=���҃19�.�\"Uթ5$	��@��cm�i','accepted');

/*Table structure for table `patient` */

DROP TABLE IF EXISTS `patient`;

CREATE TABLE `patient` (
  `sno` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `age` int(50) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `cpwd` varchar(100) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  `mobile` int(10) DEFAULT NULL,
  `disease` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `patient` */

insert  into `patient`(`sno`,`name`,`email`,`age`,`pwd`,`cpwd`,`gender`,`mobile`,`disease`) values (1,'Keerthana','cse.takeoff@gmail.com',33,'123','123','Female',2147483647,'Fever');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

SET FOREIGN_KEY_CHECKS=1;
