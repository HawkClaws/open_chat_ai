from service.web_serach_engine import WebSerachEngine
from service.search_word_extractor import SearchWordExtractor

from llama_index.llms.base import LLM
from llama_index import (
    ServiceContext,
    TrafilaturaWebReader,
    SummaryIndex
)


class OpenChatAI:
    llm: LLM
    web_search_engine: WebSerachEngine
    search_word_extractor: SearchWordExtractor

    def __init__(self, llm: LLM, web_search_engine: WebSerachEngine, search_word_extractor: SearchWordExtractor) -> None:
        self.llm = llm
        self.web_search_engine = web_search_engine
        self.search_word_extractor = search_word_extractor

    def __get_urls(self, keyword)->list[str]:
        url_datas = self.web_search_engine.search(keyword)
        urls = [item.url for item in url_datas]
        return urls

    def __web_query(self, query, web_page_urls):

        # define our LLM
        service_context = ServiceContext.from_defaults(
            llm=self.llm,
            context_window=2048,
            num_output=256
        )

        # Load the your data
        documents = TrafilaturaWebReader().load_data(web_page_urls)
        index = SummaryIndex.from_documents(
            documents, service_context=service_context)

        query_engine = index.as_query_engine()
        response = query_engine.query(query)

        return response
    
    def ask(self,question):
        keyword = self.search_word_extractor.extract(question)
        urls = self.__get_urls(keyword)
        response = self.__web_query(question,urls[:3])
        return response
