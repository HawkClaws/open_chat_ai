import abc

class SearchWordExtractor(abc.ABC):
    @abc.abstractmethod
    def extract(self, sentence: str) -> str:
        pass
