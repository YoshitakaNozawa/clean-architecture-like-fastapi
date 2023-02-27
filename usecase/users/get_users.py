from werkzeug.exceptions import InternalServerError

from usecase.interfaces.presenter_interface import PresenterInterface
from usecase.interfaces.repository_gateway import RepositoryGateway
from entities.queries.user_query import UserQueryU


class GetUsers:
    """
    全ユーザー情報を取得する。

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

    def get(self) -> dict:
        """ 全ユーザー情報を取得するメインロジック """

        try:
            # クエリの実行と、結果の取得。情報を取得する。
            query: list[dict] = UserQueryU.get_users_query()
            users: list[dict] = self.repository.select(query['query'])
        except InternalServerError:
            # エラー時の返却値の設定
            return self.presenter.api_form_with_error(f"ERROR: {query}")

        # 返却値の設定
        return self.presenter.data_count(len(users)).api_form_with_data(users)
