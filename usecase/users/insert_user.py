import ulid
from werkzeug.exceptions import InternalServerError

from usecase.interfaces.presenter_interface import PresenterInterface
from usecase.interfaces.repository_gateway import RepositoryGateway
from entities.queries.user_query import UserQueryU


class InsertSelectedUser:
    """
    特定のユーザー情報を追加する。

    Attributes
    ----------
    presenter : PresenterInterface
        プレゼンター。UI(フロントへの返却データ)の形式調整を行う。
    repository : RepositoryGateway
        レポジトリ。DBへの接続に使用。

    Returns
    ----------
    self.presenter.default_api_form() : dict
        ユースケースの結果を辞書型で返す。
    """

    def __init__(self, presenter: PresenterInterface, repository: RepositoryGateway):
        self.presenter = presenter
        self.repository = repository

    def insert(self, request_body: dict) -> dict:
        """ 特定のユーザー情報を追加するメインロジック """
        new_user_id: str = str(ulid.new())
        user_name: str = request_body['user_name']
        mail_address: str = request_body['mail_address']
        password: str = request_body['password']

        try:
            # クエリの実行と、結果の取得。情報を取得する。
            query: list[dict] = UserQueryU.insert_user_query(new_user_id, user_name, mail_address, password)
            self.repository.insert(query['query'], query['values'])
        except InternalServerError:
            # エラー時の返却値の設定
            return self.presenter.api_form_with_error(f"ERROR: {query['query']}")

        # 返却値の設定
        return self.presenter.default_api_form()
