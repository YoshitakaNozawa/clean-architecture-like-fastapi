class HogeQueryU:
    @staticmethod
    def get_hoges_query() -> list[dict]:
        """ ほげ一覧を取得するSQL """
        query: list[dict] = {
            'query': """
                SELECT ULID_ENCODE(hoge_id) AS hoge_id, hoge_name
                FROM hoges;
                """
        }
        return query
