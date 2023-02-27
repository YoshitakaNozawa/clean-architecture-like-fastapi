--
-- テーブルの作成
--
CREATE TABLE IF NOT EXISTS `hoges` (
  `hoge_id` binary(16) NOT NULL,
  `hoge_name` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`hoge_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

--
-- テストデータのインサート
--
INSERT INTO `hoges` (`hoge_id`, `hoge_name`) VALUES
(ULID_DECODE('01GB7BTNVS6Y3HWK302V9GCQ7W'), 'hoge name1'),
(ULID_DECODE('01GB7BTSGRRK3C45ZZV77HH9EY'), 'hoge name2'),
(ULID_DECODE('01GB7BTX83RB3SFZ4ES9W6FDRE'), 'hoge name3');
