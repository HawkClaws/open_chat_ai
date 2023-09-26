import lxml.html
import requests

def search_keyword_yahoo(keyword):
    searched_list = []
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
            result = {'title': title, 'url': href}
            searched_list.append(result)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return searched_list

if __name__ == '__main__':
    keyword = "python YAHOO! JAPAN検索"
    search_results = search_keyword_yahoo(keyword)
    print(search_results)
    for result in search_results:
        print(result)
