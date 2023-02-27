from abc import ABCMeta, abstractmethod


class PresenterInterface(metaclass=ABCMeta):
    """ プレゼンターのインターフェース """

    @abstractmethod
    def is_success(self, is_success: bool):
        pass

    @abstractmethod
    def message(self, message: str):
        pass

    @abstractmethod
    def data_count(self, data_count: int):
        pass

    @abstractmethod
    def default_api_form(self) -> dict:
        pass

    @abstractmethod
    def api_form_with_data(self, data_dict: dict) -> dict:
        pass

    @abstractmethod
    def api_form_with_error(self, error_message: str) -> dict:
        pass
