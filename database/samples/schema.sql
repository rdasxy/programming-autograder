SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `barterbids`;
CREATE TABLE IF NOT EXISTS `barterbids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `barter_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(100) CHARACTER SET latin1 NOT NULL,
  `description` text CHARACTER SET latin1 NOT NULL,
  `updated` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_barterbids_barters` (`barter_id`),
  KEY `fk_barterbids_users` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=34 ;

DROP TABLE IF EXISTS `barters`;
CREATE TABLE IF NOT EXISTS `barters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `location` text NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  `open` tinyint(4) NOT NULL DEFAULT '1',
  `completed` tinyint(1) NOT NULL DEFAULT '0',
  `offered` tinyint(11) NOT NULL,
  `bid_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_barters_user` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

DROP TABLE IF EXISTS `communityprojects`;
CREATE TABLE IF NOT EXISTS `communityprojects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `location` text NOT NULL,
  `description` text NOT NULL,
  `estimatedMinutes` int(11) NOT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  `progress` decimal(10,0) DEFAULT NULL,
  `minutesCompleted` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_communityprojects_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `experiences`;
CREATE TABLE IF NOT EXISTS `experiences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `skill_id` int(11) NOT NULL,
  `title` text NOT NULL,
  `month` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_experiences_skills` (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `invitees`;
CREATE TABLE IF NOT EXISTS `invitees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `inviter_id` int(11) NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `inviters`;
CREATE TABLE IF NOT EXISTS `inviters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `updated` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=17 ;

DROP TABLE IF EXISTS `jobbids`;
CREATE TABLE IF NOT EXISTS `jobbids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_id` int(11) NOT NULL,
  `description` text CHARACTER SET latin1,
  `amount` decimal(11,0) NOT NULL,
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=10 ;

DROP TABLE IF EXISTS `jobs`;
CREATE TABLE IF NOT EXISTS `jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `description` text,
  `location` varchar(45) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime DEFAULT NULL,
  `open` tinyint(4) NOT NULL DEFAULT '1',
  `completed` tinyint(4) NOT NULL DEFAULT '0',
  `budgetMin` decimal(10,0) DEFAULT NULL,
  `budgetMax` decimal(10,0) DEFAULT NULL,
  `preferredBudget` decimal(10,0) DEFAULT NULL,
  `bid_count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_jobs_users` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

DROP TABLE IF EXISTS `ratings`;
CREATE TABLE IF NOT EXISTS `ratings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) NOT NULL,
  `post_category` varchar(100) NOT NULL,
  `id_of_posters_rating` int(11) DEFAULT NULL,
  `id_of_doers_rating` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ratings_users1` (`id_of_posters_rating`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `ratings_tables`;
CREATE TABLE IF NOT EXISTS `ratings_tables` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `is_poster` tinyint(1) NOT NULL,
  `post_category` varchar(100) NOT NULL,
  `post_id` int(11) NOT NULL,
  `field` varchar(100) NOT NULL,
  `rating` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_ratings_tables_users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `skills`;
CREATE TABLE IF NOT EXISTS `skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(45) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `fk_skills_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `email` text NOT NULL,
  `school` text,
  `superuser` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  `picture` varchar(250) DEFAULT NULL,
  `website` varchar(250) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;


ALTER TABLE `barterbids`
  ADD CONSTRAINT `fk_barterbids_barters` FOREIGN KEY (`barter_id`) REFERENCES `barters` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_barterbids_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `barters`
  ADD CONSTRAINT `fk_barters_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `communityprojects`
  ADD CONSTRAINT `fk_communityprojects_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `experiences`
  ADD CONSTRAINT `fk_experiences_skills` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `jobbids`
  ADD CONSTRAINT `jobbids_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`);

ALTER TABLE `jobs`
  ADD CONSTRAINT `fk_jobs_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `skills`
  ADD CONSTRAINT `fk_skills_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `invitees` 
  ADD FOREIGN KEY ( `inviter_id` ) REFERENCES `inviters`( `id` ) ON DELETE CASCADE ON UPDATE CASCADE;
