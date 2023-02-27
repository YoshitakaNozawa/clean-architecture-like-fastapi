--
-- テーブルの作成
--
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` binary(16) NOT NULL,
  `user_name` varchar(20) NOT NULL DEFAULT '',
  `mail_address` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

--
-- テストデータのインサート
--
INSERT INTO `users` (`user_id`, `user_name`, `mail_address`, `password`) VALUES
(ULID_DECODE('01G921E9GQVWZN4MRWYJSS21P3'), '毎日 寝太郎', 'test_user1@test.com', 'password1'),
(ULID_DECODE('01GB6SC5PDBEC0PFDFHJ913QZ5'), '車田 テスラ', 'test_user2@test.com', 'password2'),
(ULID_DECODE('01GB6SC9BH6RF5NCXA0887Q5C9'), '金　肉尾', 'test_user3@test.com', 'password3');
