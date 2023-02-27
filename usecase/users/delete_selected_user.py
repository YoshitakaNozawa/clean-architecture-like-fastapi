from werkzeug.exceptions import InternalServerError

from usecase.interfaces.presenter_interface import PresenterInterface
from usecase.interfaces.repository_gateway import RepositoryGateway
from entities.queries.user_query import UserQueryU


class DeleteSelectedUser:
    """
    特定のユーザーを削除する。

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

    def delete(self, user_id: str) -> dict:
        """ 特定のユーザーを削除するメインロジック """
        try:
            # クエリの実行と、結果の取得。情報を取得する。
            query: list[dict] = UserQueryU.delete_user_query(user_id)
            self.repository.delete(query['query'], query['values'])
        except InternalServerError:
            # エラー時の返却値の設定
            return self.presenter.api_form_with_error(f"ERROR: {query}")

        # 返却値の設定
        return self.presenter.default_api_form()
