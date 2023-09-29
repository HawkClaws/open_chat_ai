from model.url_model import URLModel
import abc

class WebSerachEngine(abc.ABC):
    @abc.abstractmethod
    def search(self, keyword: str) -> list[URLModel]:
        pass
