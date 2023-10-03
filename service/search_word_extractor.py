from llama_index.llms.base import LLM
from litellm import completion
import re
import ast
import logging
from typing import Any
import time

logger = logging.getLogger(__name__)


class SearchWordExtractor():
    def extract(self, sentence: str) -> str:
        max_retries = 3  # リトライする最大回数を設定
        retry_count = 0  # 現在のリトライ回数を初期化

        while retry_count < max_retries:
            try:
                # ここに例外が発生する可能性のあるコードを書く
                result = self.completion_web_search_word(sentence)  # 例外が発生するかもしれない関数の例
                break  # 例外が発生しなかった場合、ループを抜けます
            except Exception as e:
                print(f"An exception occurred: {e}")
                retry_count += 1  # リトライ回数を増やす
                if retry_count < max_retries:
                    print(f"Retrying attempt {retry_count}/{max_retries}...")
                    time.sleep(1)  # エラーメッセージを表示してからリトライまで待つ

        if retry_count == max_retries:
            raise Exception(f"Reached the maximum retry count of {max_retries}. Aborting the process.")
        return result
    
    def completion_web_search_word(self, sentence: str):
        content = f"""
        あなたは、自然言語処理をするために設計されたAIモデルです

次の問題を解決するためにウェブ検索を行います
問題を解決するために必要なウェブ検索ワードを回答してください

### 問題

{sentence}
"""+"""
### 回答方法

厳密には**JSONで応答**する。JSONは、以下のTypeScriptのResponse型に対応している必要がある:
interface Response {
//ウェブ検索ワード
webSearchWord: string;
}

先に指定した**JSONスキーマを使って応答**する:
"""
        messages = [{"content": content, "role": "user"}]

        # openai call
        response = completion("gpt-3.5-turbo", messages)
        res_content = response['choices'][0]['message']['content']
        result = self.extract_dict_from_response(res_content)
        return result.get('webSearchWord')
    def extract_dict_from_response(self, response_content: str) -> dict[str, Any]:
        # Sometimes the response includes the JSON in a code block with ```
        pattern = r'```([\s\S]*?)```'
        match = re.search(pattern, response_content)

        if match:
            response_content = match.group(1).strip()
            # Remove language names in code blocks
            response_content = response_content.lstrip("json")
        else:
            # The string may contain JSON.
            json_pattern = r'{.*}'
            match = re.search(json_pattern, response_content)

            if match:
                response_content = match.group()

        # response content comes from OpenAI as a Python `str(content_dict)`, literal_eval reverses this
        try:
            return ast.literal_eval(response_content)
        except BaseException as e:
            logger.info(f"Error parsing JSON response with literal_eval {e}")
            logger.debug(f"Invalid JSON received in response: {response_content}")
            # TODO: How to raise an error here without causing the program to exit?
            return {}