# ChatGPTから502エラーが返る場合は下記をコメントアウト
from os import environ
environ['CHATGPT_BASE_URL'] = 'https://ai.fakeopen.com/api/'

# ChatGPTのアクセストークンの入力　詳細は https://github.com/acheong08/ChatGPT#--access-token を参照
ACCESS_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

from datetime import datetime
from llama_index.llms.base import llm_completion_callback
from llama_index.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)

from llama_index import (
    ServiceContext,
    SimpleDirectoryReader, 
    TrafilaturaWebReader,
    SummaryIndex
)
from typing import Any
from revChatGPT.V1 import Chatbot

chatbot = Chatbot(config={
    "access_token": ACCESS_TOKEN,
})


# set context window size
context_window = 2048
# set number of output tokens
num_output = 256

# store the pipeline/model outisde of the LLM class to avoid memory issues(HaggingFaceのpipelineを使うわけではないので、何でもいい)
model_name = "acheong08/ChatGPT"

class revChatGPTLLM(CustomLLM):

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=context_window,
            num_output=num_output,
            model_name=model_name
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = ""
        for data in chatbot.ask(
            prompt
        ):
            response = data["message"]

        return CompletionResponse(text=response)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        raise NotImplementedError()


def web_query(query,web_page_urls):

    # define our LLM
    llm = revChatGPTLLM()

    service_context = ServiceContext.from_defaults(
        llm=llm,
        context_window=context_window,
        num_output=num_output
    )

    # Load the your data
    # documents = SimpleDirectoryReader(
    #     input_files=["dataset.txt"]
    # ).load_data()
    documents = TrafilaturaWebReader().load_data(web_page_urls)
    index = SummaryIndex.from_documents(documents, service_context=service_context)

    # Query and print response
    print(f"{str(datetime.now())} : Start Query")
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    print(response)
    print(f"{str(datetime.now())} : End Query")
    return response