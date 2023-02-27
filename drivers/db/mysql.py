from usecase.interfaces.repository_gateway import RepositoryGateway
from logging import getLogger
import sqlalchemy


class Mysql(RepositoryGateway):
    """ クエリを実行し、結果を返すクラス """

    logger = getLogger(__name__)

    def __init__(self):
        self._db_engine: str = 'mysql'
        self._db_client: str = 'pymysql'
        self._user_name: str = 'user_name'
        self._password: str = 'password'
        self._db_endpoint: str = 'mysql'
        self._db_port: str = '3306'
        self._db_name: str = 'testdb'

    def conn(self):
        """ DBへ接続する """
        database_url: str = '{}+{}://{}:{}@{}:{}/{}'.format(
            self._db_engine,
            self._db_client,
            self._user_name,
            self._password,
            self._db_endpoint,
            self._db_port,
            self._db_name
        )
        return sqlalchemy.create_engine(database_url).connect()

    def select(self, query: str, *replacers) -> list[dict]:
        """ 任意のパラメータを置換し、任意のクエリを実行し、結果を取得する """
        with self.conn() as con:
            try:
                result = con.execute(sqlalchemy.sql.text(query), *replacers).all()
            except Exception as e:
                self.logger.error(f'Failed to execute query: {query}')
                raise e
            else:
                return self._convert_to_dict_list(result)

    def insert(self, query: str, *replacers):
        """ 任意のクエリを実行する """
        self._no_response_execute(query, *replacers)

    def update(self, query: str, *replacers):
        """ 任意のクエリを実行する """
        self._no_response_execute(query, *replacers)

    def delete(self, query: str, *replacers):
        """ 任意のクエリを実行する """
        self._no_response_execute(query, *replacers)

    def _no_response_execute(self, query, *replacers):
        with self.conn() as con:
            try:
                con.execute(sqlalchemy.sql.text(query), *replacers)
            except Exception as e:
                self.logger.error(f'Failed to execute query: {query}')
                raise e

    def _convert_to_dict_list(self, ls: list) -> list[dict]:
        """ selectで取得した結果を辞書型のリストに変換する """
        dict_list = []
        for elm in ls:
            new_dict = dict()
            for key, value in elm.items():
                new_dict[key] = value
            dict_list.append(new_dict)

        return dict_list
