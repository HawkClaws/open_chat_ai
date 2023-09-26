from get_urls_by_yahoo import search_keyword_yahoo
from revChatGPTLLM import web_query

query = "WBCでの大谷翔平の活躍は？"
data = search_keyword_yahoo(query)
urls = [item['url'] for item in data]

response = web_query(query, urls[:3])
print(response)
