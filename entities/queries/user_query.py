class UserQueryU:
    @staticmethod
    def get_users_query() -> list[dict]:
        """ 全ユーザー情報を取得するSQL """
        query: list[dict] = {
            'query': """
                SELECT ULID_ENCODE(user_id) AS user_id, user_name, mail_address
                FROM users;
                """
        }
        return query

    @staticmethod
    def get_selected_user_query(user_id: str) -> list[dict]:
        """ 特定のユーザー情報を取得するSQL """
        query: list[dict] = {
            'query': f"""
                SELECT ULID_ENCODE(user_id) AS user_id, user_name, mail_address 
                FROM users 
                WHERE user_id = ULID_DECODE(:user_id);
                """,
            'values': {
                'user_id': user_id
            }
        }
        return query

    @staticmethod
    def update_selected_user_query(user_id: str, user_name: str, mail_address: str, password: str) -> list[dict]:
        """ 特定のユーザー情報を更新するSQL """
        query: list[dict] = {
            'query': f"""
                UPDATE users 
                SET user_name=:user_name, mail_address=:mail_address, password=:password 
                WHERE user_id = ULID_DECODE(:user_id);
                """,
            'values': {
                'user_id': user_id,
                'user_name': user_name,
                'mail_address': mail_address,
                'password': password
            }
        }
        return query

    @staticmethod
    def insert_user_query(user_id: str, user_name: str, mail_address: str, password: str) -> list[dict]:
        """ ユーザー情報を追加するSQL """
        query: list[dict] = {
            'query': f"""
                INSERT INTO users (user_id, user_name, mail_address, password)
                VALUES (ULID_DECODE(:user_id), :user_name, :mail_address, :password);
                """,
            'values': {
                'user_id': user_id,
                'user_name': user_name,
                'mail_address': mail_address,
                'password': password
            }
        }
        return query

    @staticmethod
    def delete_user_query(user_id: str) -> list[dict]:
        """ ユーザー情報を追加するSQL """
        query: list[dict] = {
            'query': f"""
                DELETE FROM users 
                WHERE user_id = ULID_DECODE(:user_id);
                """,
            'values': {
                'user_id': user_id
            }
        }
        return query
