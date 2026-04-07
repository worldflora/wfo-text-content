CREATE TABLE `global_zones` (
  `key` varchar(40) NOT NULL,
  `wfo_id` varchar(14) NOT NULL,
  `zone` varchar(20) NOT NULL,
  `wcvp_name` varchar(100) NOT NULL,
  `wcvp_name_id` int NOT NULL,
  `occurrence_count` int NOT NULL DEFAULT '1',
  `occurrences` text,
  PRIMARY KEY (`key`),
  UNIQUE KEY `key_UNIQUE` (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
