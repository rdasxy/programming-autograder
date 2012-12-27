SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `SCE-AutoGrdr` DEFAULT CHARACTER SET latin1 ;
USE `SCE-AutoGrdr` ;

DROP TABLE IF EXISTS `SCE-AutoGrdr`.`Attempts` ;
CREATE TABLE `Attempts` (
	`UserId` VARCHAR(15) NOT NULL,
	`CourseNumber` VARCHAR(6) NOT NULL,
	`Timestamp` DATETIME NOT NULL,
	`ProblemNumber` INT(11) NOT NULL,
	`Outcome` VARCHAR(12) NOT NULL
)
ENGINE = InnoDB;
`Courses`
DROP TABLE IF EXISTS `SCE-AutoGrdr`.`Courses` ;
CREATE TABLE `Courses` (
	`CourseNumber` VARCHAR(6) NOT NULL,
	`CourseTitle` VARCHAR(24) NOT NULL,
	PRIMARY KEY (`CourseNumber`)
)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `SCE-AutoGrdr`.`JobFiles` ;
CREATE TABLE `JobFiles` (
	`JobNumber` INT(11) NOT NULL,
	`FileName` VARCHAR(24) NOT NULL,
	`FileContents` MEDIUMTEXT NOT NULL
)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `SCE-AutoGrdr`.`Jobs` ;
CREATE TABLE `Jobs` (
	`Userid` VARCHAR(6) NOT NULL,
	`CourseNumber` VARCHAR(6) NOT NULL,
	`ProblemNumber` INT(11) NOT NULL,
	`ProblemID` INT(11) NOT NULL,
	`Status` VARCHAR(12) NOT NULL,
	`SequenceNumber` INT(11) NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (`SequenceNumber`)
)
ENGINE = InnoDB;

DROP TABLE IF EXISTS `SCE-AutoGrdr`.`Problems` ;
CREATE TABLE `Problems` (
	`ProblemId` INT(11) NOT NULL,
	`CourseNumber` VARCHAR(6) NOT NULL,
	`ProblemNumber` INT(11) NOT NULL,
	`Title` TEXT NOT NULL,
	`Description` TEXT NOT NULL,
	`NumFiles` INT(11) NOT NULL,
	PRIMARY KEY (`ProblemNumber`, `CourseNumber`)
)
ENGINE = InnoDB;


DROP TABLE IF EXISTS `SCE-AutoGrdr`.`Roll` ;
CREATE TABLE `Roll` (
	`CourseNumber` VARCHAR(6) NOT NULL,
	`SectionNumber` VARCHAR(4) NULL DEFAULT NULL COMMENT 'NULL for isntructors, TAs, students granted permission.',
	`UserID` VARCHAR(15) NOT NULL,
	`UUID` VARCHAR(24) NOT NULL,
	`FirstName` VARCHAR(15) NOT NULL,
	`LastName` VARCHAR(15) NOT NULL,
	PRIMARY KEY (`CourseNumber`, `UserID`)
)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;