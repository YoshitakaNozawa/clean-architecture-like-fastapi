from typing import Optional

from usecase.interfaces.presenter_interface import PresenterInterface


class APIResponse(PresenterInterface):
    """ UIの形式を規定するクラス """

    def __init__(self):
        self._is_success: bool = True
        self._message: str = ""
        self._data_count: Optional[int] = 0

    def is_success(self, is_success: bool):
        """ is_successのデータをインスタンスに記録 """
        self._is_success = is_success
        return self

    def message(self, message: str):
        """ messageのデータをインスタンスに記録 """
        self._message = message
        return self

    def data_count(self, data_count: int):
        """ data_countのデータをインスタンスに記録 """
        self._data_count = data_count
        return self

    def default_api_form(self) -> dict:
        """ デフォルトのレスポンスjsonを返す """
        return dict(
            system=dict(
                is_success=self._is_success,
                message=self._message,
                data_count=self._data_count
            )
        )

    def api_form_with_data(self, data_dict: dict) -> dict:
        """ レスポンスjsonに"data"のdictを追加する """
        response: dict = self.default_api_form()
        response.update({"data": data_dict})
        return response

    def api_form_with_error(self, error_message: str) -> dict:
        """ error時の返却用 """
        self._is_success = False
        self._message = error_message
        response: dict = self.default_api_form()
        return response
