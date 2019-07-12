CREATE TABLE `parttimejobinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `web_type` varchar(45) DEFAULT NULL COMMENT '网站类型',
  `job_type` varchar(45) DEFAULT NULL COMMENT '兼职类型',
  `job_url` varchar(300) DEFAULT NULL COMMENT '兼职详情页面',
  `publish_info` varchar(200) DEFAULT NULL COMMENT '发布人信息',
  `job_title` varchar(200) DEFAULT NULL,
  `job_amt` varchar(45) DEFAULT NULL,
  `job_desc` varchar(500) DEFAULT NULL,
  `publish_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `job_url_UNIQUE` (`job_url`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;