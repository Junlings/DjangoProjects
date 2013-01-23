-- ----------------------------------------------------------------------
-- MySQL Migration Toolkit
-- SQL Create Script
-- ----------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `junxiaci_newlab`
  CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `junxiaci_newlab`;
-- -------------------------------------
-- Tables

DROP TABLE IF EXISTS `junxiaci_newlab`.`accounts_userprofile`;
CREATE TABLE `junxiaci_newlab`.`accounts_userprofile` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `zipcode` VARCHAR(5) NOT NULL,
  `BOXNET_FolderID` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`accounts_userref`;
CREATE TABLE `junxiaci_newlab`.`accounts_userref` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `object_type` VARCHAR(20) NOT NULL,
  `object_LB` VARCHAR(20) NOT NULL,
  `note` LONGTEXT NOT NULL,
  `addon` DATETIME NOT NULL,
  `addby_id` INT(11) NULL,
  `Lib_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `accounts_userref_6f551959` (`addby_id`),
  INDEX `accounts_userref_784677ae` (`Lib_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`accounts_userreflib`;
CREATE TABLE `junxiaci_newlab`.`accounts_userreflib` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `Owner_id` INT(11) NOT NULL,
  `addon` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `accounts_userreflib_5be504d0` (`Owner_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`accounts_userreflib_contributor`;
CREATE TABLE `junxiaci_newlab`.`accounts_userreflib_contributor` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `userreflib_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `userreflib_id` (`userreflib_id`, `user_id`),
  INDEX `accounts_userreflib_Contributor` (`userreflib_id`),
  INDEX `accounts_userreflib_Contributor` (`user_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_group`;
CREATE TABLE `junxiaci_newlab`.`auth_group` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_group_permissions`;
CREATE TABLE `junxiaci_newlab`.`auth_group_permissions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `group_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `group_id` (`group_id`, `permission_id`),
  INDEX `auth_group_permissions_425ae3c4` (`group_id`),
  INDEX `auth_group_permissions_1e014c8f` (`permission_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_message`;
CREATE TABLE `junxiaci_newlab`.`auth_message` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `message` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `auth_message_403f60f` (`user_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_permission`;
CREATE TABLE `junxiaci_newlab`.`auth_permission` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL,
  `content_type_id` INT(11) NOT NULL,
  `codename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `content_type_id` (`content_type_id`, `codename`),
  INDEX `auth_permission_1bb8f392` (`content_type_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_user`;
CREATE TABLE `junxiaci_newlab`.`auth_user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(30) NOT NULL,
  `first_name` VARCHAR(30) NOT NULL,
  `last_name` VARCHAR(30) NOT NULL,
  `email` VARCHAR(75) NOT NULL,
  `password` VARCHAR(128) NOT NULL,
  `is_staff` TINYINT(1) NOT NULL,
  `is_active` TINYINT(1) NOT NULL,
  `is_superuser` TINYINT(1) NOT NULL,
  `last_login` DATETIME NOT NULL,
  `date_joined` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username` (`username`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_user_groups`;
CREATE TABLE `junxiaci_newlab`.`auth_user_groups` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `group_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id`, `group_id`),
  INDEX `auth_user_groups_403f60f` (`user_id`),
  INDEX `auth_user_groups_425ae3c4` (`group_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`auth_user_user_permissions`;
CREATE TABLE `junxiaci_newlab`.`auth_user_user_permissions` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `permission_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id`, `permission_id`),
  INDEX `auth_user_user_permissions_403f` (`user_id`),
  INDEX `auth_user_user_permissions_1e01` (`permission_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conference`;
CREATE TABLE `junxiaci_newlab`.`conference_conference` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `T2` VARCHAR(400) NULL,
  `CY` VARCHAR(200) NULL,
  `PY` VARCHAR(4) NULL,
  `DA` VARCHAR(20) NULL,
  `PB_id` INT(11) NULL,
  `C1` VARCHAR(200) NULL,
  `LA` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  INDEX `conference_conference_1cc1f958` (`PB_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conferencepaper`;
CREATE TABLE `junxiaci_newlab`.`conference_conferencepaper` (
  `publication_ptr_id` INT(11) NOT NULL,
  `conference_id` INT(11) NULL,
  `proceeding_id` INT(11) NULL,
  `TI` VARCHAR(400) NULL,
  `TT` VARCHAR(400) NULL,
  `ST` VARCHAR(400) NULL,
  `AB` LONGTEXT NULL,
  `VL` VARCHAR(5) NULL,
  `SP` VARCHAR(20) NULL,
  `M1` VARCHAR(20) NULL,
  `UR` VARCHAR(200) NULL,
  `Y2` VARCHAR(20) NULL,
  `SN` VARCHAR(20) NULL,
  `DO` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `CA` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`),
  INDEX `conference_conferencepaper_5cb6` (`conference_id`),
  INDEX `conference_conferencepaper_580f` (`proceeding_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conferencepaper_tas`;
CREATE TABLE `junxiaci_newlab`.`conference_conferencepaper_tas` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `conferencepaper_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `conferencepaper_id` (`conferencepaper_id`, `authors_id`),
  INDEX `conference_conferencepaper_TAs_` (`conferencepaper_id`),
  INDEX `conference_conferencepaper_TAs_` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conferenceproceeding`;
CREATE TABLE `junxiaci_newlab`.`conference_conferenceproceeding` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `conference_id` INT(11) NULL,
  `C3` VARCHAR(500) NULL,
  `C2` VARCHAR(4) NULL,
  `NV` VARCHAR(5) NULL,
  `ST` VARCHAR(200) NULL,
  `C5` VARCHAR(20) NULL,
  `T3` VARCHAR(200) NULL,
  `ET` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  INDEX `conference_conferenceproceeding` (`conference_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conferenceproceeding_a3`;
CREATE TABLE `junxiaci_newlab`.`conference_conferenceproceeding_a3` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `conferenceproceeding_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `conferenceproceeding_id` (`conferenceproceeding_id`, `authors_id`),
  INDEX `conference_conferenceproceeding` (`conferenceproceeding_id`),
  INDEX `conference_conferenceproceeding` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`conference_conferenceproceeding_a4`;
CREATE TABLE `junxiaci_newlab`.`conference_conferenceproceeding_a4` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `conferenceproceeding_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `conferenceproceeding_id` (`conferenceproceeding_id`, `authors_id`),
  INDEX `conference_conferenceproceeding` (`conferenceproceeding_id`),
  INDEX `conference_conferenceproceeding` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_address`;
CREATE TABLE `junxiaci_newlab`.`contributor_address` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(100) NOT NULL,
  `country` VARCHAR(100) NOT NULL,
  `state` VARCHAR(100) NOT NULL,
  `city` VARCHAR(100) NOT NULL,
  `address_line1` VARCHAR(100) NOT NULL,
  `address_line2` VARCHAR(100) NULL,
  `zipcode` VARCHAR(100) NOT NULL,
  `notes` LONGTEXT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_authors`;
CREATE TABLE `junxiaci_newlab`.`contributor_authors` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `firstname` VARCHAR(200) NOT NULL,
  `lastname` VARCHAR(200) NOT NULL,
  `middlename` VARCHAR(200) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_authors_address`;
CREATE TABLE `junxiaci_newlab`.`contributor_authors_address` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `authors_id` INT(11) NOT NULL,
  `address_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `authors_id` (`authors_id`, `address_id`),
  INDEX `contributor_authors_address_200` (`authors_id`),
  INDEX `contributor_authors_address_4de` (`address_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_authors_contacts`;
CREATE TABLE `junxiaci_newlab`.`contributor_authors_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `authors_id` INT(11) NOT NULL,
  `contacts_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `authors_id` (`authors_id`, `contacts_id`),
  INDEX `contributor_authors_contacts_20` (`authors_id`),
  INDEX `contributor_authors_contacts_31` (`contacts_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_contacts`;
CREATE TABLE `junxiaci_newlab`.`contributor_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(20) NULL,
  `phone` VARCHAR(100) NULL,
  `fax` VARCHAR(100) NULL,
  `email` VARCHAR(75) NULL,
  `website` VARCHAR(100) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_publisher`;
CREATE TABLE `junxiaci_newlab`.`contributor_publisher` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NOT NULL,
  `shortname` VARCHAR(200) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_publisher_address`;
CREATE TABLE `junxiaci_newlab`.`contributor_publisher_address` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `publisher_id` INT(11) NOT NULL,
  `address_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `publisher_id` (`publisher_id`, `address_id`),
  INDEX `contributor_publisher_address_2` (`publisher_id`),
  INDEX `contributor_publisher_address_4` (`address_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_publisher_contacts`;
CREATE TABLE `junxiaci_newlab`.`contributor_publisher_contacts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `publisher_id` INT(11) NOT NULL,
  `contacts_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `publisher_id` (`publisher_id`, `contacts_id`),
  INDEX `contributor_publisher_contacts_` (`publisher_id`),
  INDEX `contributor_publisher_contacts_` (`contacts_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_socialmedia`;
CREATE TABLE `junxiaci_newlab`.`contributor_socialmedia` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `facebook` VARCHAR(100) NULL,
  `linkedin` VARCHAR(100) NULL,
  `twitter` VARCHAR(100) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_socialmedia_china`;
CREATE TABLE `junxiaci_newlab`.`contributor_socialmedia_china` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `sina_weibo` VARCHAR(100) NULL,
  `qq` VARCHAR(20) NULL,
  `mitbbs_id` VARCHAR(100) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`contributor_test`;
CREATE TABLE `junxiaci_newlab`.`contributor_test` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`django_admin_log`;
CREATE TABLE `junxiaci_newlab`.`django_admin_log` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `action_time` DATETIME NOT NULL,
  `user_id` INT(11) NOT NULL,
  `content_type_id` INT(11) NULL,
  `object_id` LONGTEXT NULL,
  `object_repr` VARCHAR(200) NOT NULL,
  `action_flag` SMALLINT(5) unsigned NOT NULL,
  `change_message` LONGTEXT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `django_admin_log_403f60f` (`user_id`),
  INDEX `django_admin_log_1bb8f392` (`content_type_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`django_content_type`;
CREATE TABLE `junxiaci_newlab`.`django_content_type` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `app_label` VARCHAR(100) NOT NULL,
  `model` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `app_label` (`app_label`, `model`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`django_session`;
CREATE TABLE `junxiaci_newlab`.`django_session` (
  `session_key` VARCHAR(40) NOT NULL,
  `session_data` LONGTEXT NOT NULL,
  `expire_date` DATETIME NOT NULL,
  PRIMARY KEY (`session_key`),
  INDEX `django_session_3da3d3d8` (`expire_date`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`django_site`;
CREATE TABLE `junxiaci_newlab`.`django_site` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `domain` VARCHAR(100) NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_document`;
CREATE TABLE `junxiaci_newlab`.`drafts_document` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `title` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_document_5d52dd10` (`owner_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_document_kw`;
CREATE TABLE `junxiaci_newlab`.`drafts_document_kw` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `document_id` INT(11) NOT NULL,
  `keywords_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `document_id` (`document_id`, `keywords_id`),
  INDEX `drafts_document_KW_bdd92ed` (`document_id`),
  INDEX `drafts_document_KW_7284de94` (`keywords_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_equations`;
CREATE TABLE `junxiaci_newlab`.`drafts_equations` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `file` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_equations_5d52dd10` (`owner_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_images`;
CREATE TABLE `junxiaci_newlab`.`drafts_images` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `file` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_images_5d52dd10` (`owner_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_plainparagraph`;
CREATE TABLE `junxiaci_newlab`.`drafts_plainparagraph` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_plaintext`;
CREATE TABLE `junxiaci_newlab`.`drafts_plaintext` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `context` LONGTEXT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_sections`;
CREATE TABLE `junxiaci_newlab`.`drafts_sections` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqequation`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqequation` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `equation_id` INT(11) NOT NULL,
  `paragraph_id` INT(11) NOT NULL,
  `seq_local` INT(10) unsigned NULL,
  `seq_global` INT(10) unsigned NULL,
  `caption` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqequation_19e3b3d2` (`equation_id`),
  INDEX `drafts_seqequation_bdff9cb` (`paragraph_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqimage`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqimage` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `image_id` INT(11) NOT NULL,
  `paragraph_id` INT(11) NOT NULL,
  `seq_local` INT(10) unsigned NULL,
  `seq_global` INT(10) unsigned NULL,
  `caption` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqimage_6682136` (`image_id`),
  INDEX `drafts_seqimage_bdff9cb` (`paragraph_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqparagraph`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqparagraph` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `paragraphs_id` INT(11) NOT NULL,
  `section_id` INT(11) NOT NULL,
  `seq` INT(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqparagraph_e296141` (`paragraphs_id`),
  INDEX `drafts_seqparagraph_3ff842a6` (`section_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqsection`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqsection` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `section_id` INT(11) NOT NULL,
  `document_id` INT(11) NOT NULL,
  `seq1` INT(10) unsigned NULL,
  `seq2` INT(10) unsigned NULL,
  `seq3` INT(10) unsigned NULL,
  `seq4` INT(10) unsigned NULL,
  `caption` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqsection_3ff842a6` (`section_id`),
  INDEX `drafts_seqsection_bdd92ed` (`document_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqtable`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqtable` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `table_id` INT(11) NOT NULL,
  `paragraph_id` INT(11) NOT NULL,
  `seq_local` INT(10) unsigned NULL,
  `seq_global` INT(10) unsigned NULL,
  `caption` VARCHAR(200) NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqtable_3f3c6161` (`table_id`),
  INDEX `drafts_seqtable_bdff9cb` (`paragraph_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_seqtext`;
CREATE TABLE `junxiaci_newlab`.`drafts_seqtext` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text_id` INT(11) NOT NULL,
  `paragraph_id` INT(11) NOT NULL,
  `seq` INT(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_seqtext_4cefd83d` (`text_id`),
  INDEX `drafts_seqtext_bdff9cb` (`paragraph_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`drafts_tables`;
CREATE TABLE `junxiaci_newlab`.`drafts_tables` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `owner_id` INT(11) NOT NULL,
  `file` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `drafts_tables_5d52dd10` (`owner_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`journal_journal`;
CREATE TABLE `junxiaci_newlab`.`journal_journal` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NULL,
  `shortname` VARCHAR(100) NULL,
  `impact` VARCHAR(20) NULL,
  `peroidic` VARCHAR(10) NULL,
  `nation` VARCHAR(30) NULL,
  `LA` VARCHAR(30) NULL,
  `publisher_id` INT(11) NULL,
  `website` VARCHAR(100) NULL,
  `notes` LONGTEXT NULL,
  PRIMARY KEY (`id`),
  INDEX `journal_journal_22dd9c39` (`publisher_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`journal_journalarticle`;
CREATE TABLE `junxiaci_newlab`.`journal_journalarticle` (
  `publication_ptr_id` INT(11) NOT NULL,
  `M3` VARCHAR(20) NULL,
  `T2_id` INT(11) NULL,
  `PY` VARCHAR(4) NULL,
  `VL` VARCHAR(5) NULL,
  `IS` VARCHAR(5) NULL,
  `SP` VARCHAR(20) NULL,
  `M2` VARCHAR(5) NULL,
  `TI` VARCHAR(800) NULL,
  `ST` VARCHAR(800) NULL,
  `AB` LONGTEXT NULL,
  `UR` VARCHAR(200) NULL,
  `Y2` VARCHAR(20) NULL,
  `ET` VARCHAR(20) NULL,
  `SN` VARCHAR(20) NULL,
  `C2` VARCHAR(20) NULL,
  `DO` VARCHAR(20) NULL,
  `C7` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `C6` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `RI` VARCHAR(20) NULL,
  `CA` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `C1` VARCHAR(20) NULL,
  `J2` VARCHAR(20) NULL,
  `OP` VARCHAR(20) NULL,
  `RP` VARCHAR(20) NULL,
  `TT` VARCHAR(20) NULL,
  `TA` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `DA` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`),
  INDEX `journal_journalarticle_2646796c` (`T2_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_choice`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_choice` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `question_id` INT(11) NOT NULL,
  `text` VARCHAR(500) NOT NULL,
  `order` INT(11) NULL,
  `image` VARCHAR(100) NULL,
  `_order` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `lreviews_2_choice_1f92e550` (`question_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_reviewproj`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_reviewproj` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `shortname` VARCHAR(100) NOT NULL,
  `slug` VARCHAR(255) NOT NULL,
  `topics` LONGTEXT NOT NULL,
  `associateLab_id` INT(11) NULL,
  `visible` TINYINT(1) NOT NULL,
  `image` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `slug` (`slug`),
  INDEX `lreviews_2_reviewproj_e104877` (`associateLab_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_reviewproj_contributors`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_reviewproj_contributors` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `reviewproj_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `reviewproj_id` (`reviewproj_id`, `user_id`),
  INDEX `lreviews_2_reviewproj_contribut` (`reviewproj_id`),
  INDEX `lreviews_2_reviewproj_contribut` (`user_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_reviewproj_managers`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_reviewproj_managers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `reviewproj_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `reviewproj_id` (`reviewproj_id`, `user_id`),
  INDEX `lreviews_2_reviewproj_managers_` (`reviewproj_id`),
  INDEX `lreviews_2_reviewproj_managers_` (`user_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_reviewquestion`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_reviewquestion` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `project_id` INT(11) NOT NULL,
  `question` VARCHAR(500) NOT NULL,
  `qtype` VARCHAR(2) NOT NULL,
  `order` INT(11) NULL,
  `required` TINYINT(1) NOT NULL,
  `image` VARCHAR(100) NULL,
  `choice_num_min` INT(11) NULL,
  `choice_num_max` INT(11) NULL,
  PRIMARY KEY (`id`),
  INDEX `lreviews_2_reviewquestion_499df` (`project_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`lreviews_2_singlereviews`;
CREATE TABLE `junxiaci_newlab`.`lreviews_2_singlereviews` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `object_type` VARCHAR(20) NOT NULL,
  `object_LB` VARCHAR(20) NOT NULL,
  `type` VARCHAR(50) NULL,
  `reviewer_id` INT(11) NOT NULL,
  `question_id` INT(11) NULL,
  `reviews` LONGTEXT NULL,
  `addon` DATETIME NOT NULL,
  `modifiedon` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `lreviews_2_singlereviews_2f0e81` (`reviewer_id`),
  INDEX `lreviews_2_singlereviews_1f92e5` (`question_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_authorship`;
CREATE TABLE `junxiaci_newlab`.`publications_authorship` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `author_id` INT(11) NOT NULL,
  `publication_id` INT(11) NOT NULL,
  `sequence` INT(10) unsigned NOT NULL,
  `communication` TINYINT(1) NULL,
  PRIMARY KEY (`id`),
  INDEX `publications_authorship_337b96ff` (`author_id`),
  INDEX `publications_authorship_7a9b1e55` (`publication_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book`;
CREATE TABLE `junxiaci_newlab`.`publications_book` (
  `publication_ptr_id` INT(11) NOT NULL,
  `PB_id` INT(11) NULL,
  `DA` VARCHAR(20) NULL,
  `M1` VARCHAR(20) NULL,
  `TI` VARCHAR(400) NULL,
  `C3` VARCHAR(20) NULL,
  `SP` VARCHAR(20) NULL,
  `ST` VARCHAR(20) NULL,
  `RP` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `NV` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `DO` VARCHAR(20) NULL,
  `CA` VARCHAR(20) NULL,
  `CY` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `J2` VARCHAR(20) NULL,
  `SN` VARCHAR(20) NULL,
  `SE` VARCHAR(20) NULL,
  `OP` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `M3` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  `TT` VARCHAR(20) NULL,
  `PY` VARCHAR(20) NULL,
  `AB` LONGTEXT NULL,
  `AD` VARCHAR(20) NULL,
  `VL` VARCHAR(20) NULL,
  `T2` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `L4` VARCHAR(20) NULL,
  `L1` VARCHAR(20) NULL,
  `ET` VARCHAR(20) NULL,
  `LA` VARCHAR(20) NULL,
  `UR` VARCHAR(20) NULL,
  `Y2` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`),
  INDEX `publications_book_1cc1f958` (`PB_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book_a2`;
CREATE TABLE `junxiaci_newlab`.`publications_book_a2` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `book_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `book_id` (`book_id`, `authors_id`),
  INDEX `publications_book_A2_752eb95b` (`book_id`),
  INDEX `publications_book_A2_20023397` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book_a3`;
CREATE TABLE `junxiaci_newlab`.`publications_book_a3` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `book_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `book_id` (`book_id`, `authors_id`),
  INDEX `publications_book_A3_752eb95b` (`book_id`),
  INDEX `publications_book_A3_20023397` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book_a4`;
CREATE TABLE `junxiaci_newlab`.`publications_book_a4` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `book_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `book_id` (`book_id`, `authors_id`),
  INDEX `publications_book_A4_752eb95b` (`book_id`),
  INDEX `publications_book_A4_20023397` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book_c4`;
CREATE TABLE `junxiaci_newlab`.`publications_book_c4` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `book_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `book_id` (`book_id`, `authors_id`),
  INDEX `publications_book_C4_752eb95b` (`book_id`),
  INDEX `publications_book_C4_20023397` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_book_ta`;
CREATE TABLE `junxiaci_newlab`.`publications_book_ta` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `book_id` INT(11) NOT NULL,
  `authors_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `book_id` (`book_id`, `authors_id`),
  INDEX `publications_book_TA_752eb95b` (`book_id`),
  INDEX `publications_book_TA_20023397` (`authors_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_keywords`;
CREATE TABLE `junxiaci_newlab`.`publications_keywords` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `KW` VARCHAR(50) NULL,
  PRIMARY KEY (`id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_publication`;
CREATE TABLE `junxiaci_newlab`.`publications_publication` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `RIS` LONGTEXT NULL,
  `label` VARCHAR(100) NOT NULL,
  `doc` VARCHAR(100) NULL,
  `doclink` VARCHAR(200) NULL,
  `created_by_id` INT(11) NULL,
  `created_on` DATETIME NOT NULL,
  `modified_by_id` INT(11) NULL,
  `updated_on` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `label` (`label`),
  INDEX `publications_publication_4a21cf` (`created_by_id`),
  INDEX `publications_publication_6162aa` (`modified_by_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_publication_kws`;
CREATE TABLE `junxiaci_newlab`.`publications_publication_kws` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `publication_id` INT(11) NOT NULL,
  `keywords_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `publication_id` (`publication_id`, `keywords_id`),
  INDEX `publications_publication_KWS_7a` (`publication_id`),
  INDEX `publications_publication_KWS_72` (`keywords_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_rprt`;
CREATE TABLE `junxiaci_newlab`.`publications_rprt` (
  `publication_ptr_id` INT(11) NOT NULL,
  `DO` VARCHAR(20) NULL,
  `AB` LONGTEXT NULL,
  `AD` VARCHAR(100) NULL,
  `T2` VARCHAR(100) NULL,
  `CA` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `CY` VARCHAR(20) NULL,
  `C6` VARCHAR(20) NULL,
  `ET` VARCHAR(20) NULL,
  `M3` VARCHAR(20) NULL,
  `L1` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `DA` VARCHAR(20) NULL,
  `VL` VARCHAR(20) NULL,
  `SP` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `Y2` VARCHAR(20) NULL,
  `LB` VARCHAR(20) NULL,
  `TT` VARCHAR(20) NULL,
  `LA` VARCHAR(20) NULL,
  `L4` VARCHAR(20) NULL,
  `J2` VARCHAR(20) NULL,
  `UR` VARCHAR(20) NULL,
  `PB_id` INT(11) NULL,
  `PY` VARCHAR(20) NULL,
  `TI` VARCHAR(400) NULL,
  `M1` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `TA` VARCHAR(20) NULL,
  `NV` VARCHAR(20) NULL,
  `SN` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`),
  INDEX `publications_rprt_1cc1f958` (`PB_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_stand`;
CREATE TABLE `junxiaci_newlab`.`publications_stand` (
  `publication_ptr_id` INT(11) NOT NULL,
  `DO` VARCHAR(20) NULL,
  `AB` LONGTEXT NULL,
  `AD` VARCHAR(20) NULL,
  `T2` VARCHAR(20) NULL,
  `CA` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `T3` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `CY` VARCHAR(20) NULL,
  `AU` VARCHAR(20) NULL,
  `SE` VARCHAR(20) NULL,
  `M3` VARCHAR(20) NULL,
  `L1` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `DA` VARCHAR(20) NULL,
  `VL` VARCHAR(20) NULL,
  `SP` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `Y2` VARCHAR(20) NULL,
  `LB` VARCHAR(20) NULL,
  `TT` VARCHAR(20) NULL,
  `LA` VARCHAR(20) NULL,
  `L4` VARCHAR(20) NULL,
  `J2` VARCHAR(20) NULL,
  `UR` VARCHAR(20) NULL,
  `PB_id` INT(11) NULL,
  `PY` VARCHAR(20) NULL,
  `TI` VARCHAR(400) NULL,
  `M1` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `TA` VARCHAR(20) NULL,
  `NV` VARCHAR(20) NULL,
  `SN` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`),
  INDEX `publications_stand_1cc1f958` (`PB_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`publications_thes`;
CREATE TABLE `junxiaci_newlab`.`publications_thes` (
  `publication_ptr_id` INT(11) NOT NULL,
  `DO` VARCHAR(20) NULL,
  `AB` LONGTEXT NULL,
  `AD` VARCHAR(20) NULL,
  `T2` VARCHAR(20) NULL,
  `CA` VARCHAR(20) NULL,
  `UR` VARCHAR(20) NULL,
  `DB` VARCHAR(20) NULL,
  `AN` VARCHAR(20) NULL,
  `CY` VARCHAR(20) NULL,
  `M3` VARCHAR(20) NULL,
  `L1` VARCHAR(20) NULL,
  `N1` VARCHAR(20) NULL,
  `DA` VARCHAR(20) NULL,
  `VL` VARCHAR(20) NULL,
  `SP` VARCHAR(20) NULL,
  `DP` VARCHAR(20) NULL,
  `CN` VARCHAR(20) NULL,
  `index` VARCHAR(20) NULL,
  `LB` VARCHAR(20) NULL,
  `TT` VARCHAR(20) NULL,
  `LA` VARCHAR(20) NULL,
  `L4` VARCHAR(20) NULL,
  `ST` VARCHAR(400) NULL,
  `PB` VARCHAR(200) NULL,
  `A3` VARCHAR(20) NULL,
  `PY` VARCHAR(4) NULL,
  `TI` VARCHAR(400) NULL,
  `M1` VARCHAR(20) NULL,
  `RN` VARCHAR(20) NULL,
  `Y2` VARCHAR(20) NULL,
  `TA` VARCHAR(20) NULL,
  PRIMARY KEY (`publication_ptr_id`)
)
ENGINE = INNODB;

DROP TABLE IF EXISTS `junxiaci_newlab`.`registration_registrationprofile`;
CREATE TABLE `junxiaci_newlab`.`registration_registrationprofile` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `activation_key` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_id` (`user_id`)
)
ENGINE = INNODB;



SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------
-- EOF

