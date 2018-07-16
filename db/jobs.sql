DROP DATABASE IF EXISTS `jobs`;
CREATE DATABASE `jobs`;
USE `jobs`;
/*
Navicat MySQL Data Transfer

Source Server         : con1
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : jobs

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-07-10 20:21:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for jobinfomation
-- ----------------------------
DROP TABLE IF EXISTS `jobinfomation`;
CREATE TABLE `jobinfomation` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `com_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_icelandic_ci DEFAULT NULL,
  `com_type` varchar(50) DEFAULT NULL,
  `com_size` varchar(20) DEFAULT NULL,
  `busi_type` varchar(100) DEFAULT NULL,
  `com_info` text,
  `com_loc_simple` varchar(50) DEFAULT NULL,
  `com_loc_detail` text,
  `job_title` varchar(100) DEFAULT NULL,
  `salary` varchar(20) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `num_of_recruits` varchar(50) DEFAULT NULL,
  `academic_require` varchar(20) DEFAULT NULL,
  `treatment` varchar(100) DEFAULT NULL,
  `job_info` text,
  `job_url` text,
  `com_url` text,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
