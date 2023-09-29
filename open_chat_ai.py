from service.web_serach_engine import WebSerachEngine
from service.implements.yahoo_web_serach_engine import YahooWebSerachEngine
from revChatGPTLLM import revChatGPTLLM
from llama_index.llms.base import LLM
from llama_index import (
    ServiceContext,
    TrafilaturaWebReader,
    SummaryIndex
)


class OpenChatLLM:
    llm: LLM
    web_search_engine: WebSerachEngine

    def __init__(self, llm: LLM, web_search_engine: WebSerachEngine) -> None:
        self.llm = llm
        self.web_search_engine = web_search_engine
        pass

    def get_urls(self, keyword):
        url_datas = self.web_search_engine.search(keyword)
        urls = [item.url for item in url_datas]
        return urls

    def web_query(self, query, web_page_urls):

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


open_chat_llm = OpenChatLLM(revChatGPTLLM(), YahooWebSerachEngine())
query = "WBCでの大谷翔平の活躍は？"
urls = open_chat_llm.get_urls(query)
response = open_chat_llm.web_query(query, urls[:3])
print(response)
