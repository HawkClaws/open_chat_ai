from service.search_word_extractor import SearchWordExtractor

class DummySearchWordExtractor(SearchWordExtractor):
    def extract(self, sentence: str) -> str:
        return sentence
