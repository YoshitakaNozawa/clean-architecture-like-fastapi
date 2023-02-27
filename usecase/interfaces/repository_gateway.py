from abc import abstractmethod, ABCMeta


class RepositoryGateway(metaclass=ABCMeta):

    @abstractmethod
    def conn(self):
        pass

    @abstractmethod
    def select(self, query: str) -> list[dict]:
        pass

    @abstractmethod
    def update(self, query: str):
        pass

    @abstractmethod
    def insert(self, query: str):
        pass

    @abstractmethod
    def delete(self, query: str):
        pass

    @abstractmethod
    def _convert_to_dict_list(self, ls: list) -> list[dict]:
        pass
