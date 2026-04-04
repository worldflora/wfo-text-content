CREATE TABLE `country_occurrences` (
  `key` varchar(20) NOT NULL,
  `wfo_id` varchar(14) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `country_name` varchar(100) NOT NULL,
  `wcvp_name` varchar(100) NOT NULL,
  `wcvp_name_id` int NOT NULL,
  `occurrence_count` int NOT NULL DEFAULT '1',
  `occurrences` text,
  PRIMARY KEY (`key`),
  UNIQUE KEY `key_UNIQUE` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

