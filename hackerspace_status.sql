CREATE TABLE `hackerspace_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_date` datetime NOT NULL,
  `duration` int(3) NOT NULL,
  `open` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
