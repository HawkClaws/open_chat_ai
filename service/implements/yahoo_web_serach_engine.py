import lxml.html
import requests
from model.url_model import URLModel
from service.web_serach_engine import WebSerachEngine

class YahooWebSerachEngine(WebSerachEngine):
    def search(self, keyword: str) -> list[URLModel]:
        url_data_list: list[URLModel] = []
        base_url = 'http://search.yahoo.co.jp/search'
        params = {'p': keyword, 'ei': 'UTF-8'}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            html = response.text
            dom = lxml.html.fromstring(html)
            a_list = dom.xpath("//div[@id='web']//li/a")

            for link in a_list:
                title = link.text_content()
                href = link.attrib["href"]
                url_data_list.append(URLModel(title=title, url=href))

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        return url_data_list
