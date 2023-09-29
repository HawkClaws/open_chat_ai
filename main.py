from service.open_chat_ai import OpenChatAI
from service.implements.yahoo_web_serach_engine import YahooWebSerachEngine
from service.implements.dummy_search_word_extractor import DummySearchWordExtractor
# from revChatGPTLLM import revChatGPTLLM
from llama_index.llms import OpenAI
import openai

openai.api_key = "{OpenAIのAPIキー}"

open_chat_llm = OpenChatAI(OpenAI(), YahooWebSerachEngine(), DummySearchWordExtractor())
query = "WBCでの大谷翔平の活躍は？"
response = open_chat_llm.ask(query)
print(response)
