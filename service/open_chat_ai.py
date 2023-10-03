from service.web_serach_engine import WebSerachEngine
from service.search_word_extractor import SearchWordExtractor

from llama_index.llms.base import LLM
from llama_index import (
    ServiceContext,
    TrafilaturaWebReader,
    GPTKeywordTableIndex
    
)
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
import logging

# ログフォーマットを指定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
        # ログ出力 - URLリストの取得
        logging.info(f'URLs retrieved for keyword "{keyword}": {urls}')
        return urls

    def __web_query(self, query:str, web_page_urls:list[str]):

        # define our LLM
        llama_debug_handler = LlamaDebugHandler()
        callback_manager = CallbackManager([llama_debug_handler])
        service_context = ServiceContext.from_defaults(
            llm=self.llm,
            context_window=2048,
            num_output=256,
            callback_manager=callback_manager
        )

        # Load the your data
        documents = TrafilaturaWebReader().load_data(web_page_urls)
        index = GPTKeywordTableIndex.from_documents(
            documents, service_context=service_context)

        query_engine = index.as_query_engine()
        response = query_engine.query(query)

        # ログ出力 - ウェブクエリ実行
        logging.info(f'Web query executed with query "{query}" on {len(web_page_urls)} web pages.')
        return response
    
    def ask(self,question):
        keyword = self.search_word_extractor.extract(question)
        urls = self.__get_urls(keyword)
        response = self.__web_query(question,urls[:3])

        # ログ出力 - ユーザーの質問と応答
        logging.info(f'User question: "{question}"')
        logging.info(f'Response received: "{response}"')
        return response
