CREATE TABLE `hackerspace_status` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `pub_date` datetime NOT NULL,
  `duration` int(3) NOT NULL,
  `open` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `hackerspace_sensors` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `name` char(128) NOT NULL,
  `value` double(12, 5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
