# Open Chat AI

Bing AI Chatライクな、ネット上から最新情報を取得し、情報を返してくれるAI チャット

## アーキテクチャ
1. `SearchWordExtractor`がInputされた文章から検索キーワードを抽出します
2. `WebSerachEngine`が検索エンジンを使用し、検索ワードでの検索結果URLリストを取得します
3. `LlamaIndex`がURLリストからウェブページの情報を取得し、LLMを使用してInputされた文章に対する回答を生成します

下記図の通り

![image](arch.drawio.png)


## 事前準備

### 本リポジトリのクローン

```sh
git clone https://github.com/HawkClaws/open_chat_ai.git
```

### ライブラリインストール

```sh
pip install llama-index
pip install openai
```

### 実行時設定(main.py)

`OpenAIのAPIキー`を設定してください

```python:main.py
openai.api_key = "{OpenAIのAPIキー}"

open_chat_llm = OpenChatAI(OpenAI(), YahooWebSerachEngine(), DummySearchWordExtractor())
query = "WBCでの大谷翔平の活躍は？"
response = open_chat_llm.ask(query)
print(response)
```

#### 詳細な実行時設定
OpenChatAIのコンストラクタは下記３つになります  

```python
llama_index.llms.base.LLM
service.web_serach_engine.WebSerachEngine
service.search_word_extractor.SearchWordExtractor
```

`llama_index.llms.base.LLM`は`llama_index`のLLMを任意に設定  
`WebSerachEngine`及び`SearchWordExtractor`は抽象基底クラスがあるため、それをベースに実装を行い設定可能です  
  
`SearchWordExtractor`は現状`DummySearchWordExtractor`を使用しています  
pke（[pke_japanese_googlecolab](https://github.com/HawkClaws/pke_japanese_googlecolab)）を使用予定ではありますが、必要なキーワードが削られてしまうなど、まだ調査不足です


## 使用方法

`python main.py` で実行できます

## 結果サンプル

### 入力値

`WBCでの大谷翔平の活躍は？`

### 出力値

```
大谷翔平はWBCで非常に印象的な活躍をし、大会全体の成功に大きく貢献しました。特に準決勝では、日本が1点を追いかける状況で、9回裏に大谷は先頭打者として2塁打を放ち、その後派手なガッツポーズで仲間たちを鼓舞しました。そして、決勝戦ではクローザーとして登場し、マイク・トラウトとの一騎討ちで盟友を大谷は投手としても28試合に登板し、166回を投げて15勝9敗、219奪三振、防御率2.33という素晴らしい成績を記録しました。同時に、打者としても157試合に出場し、586打数で160安打、34本塁打、95打点、11盗塁、打率.273を記録し、オールラウンドなプレースタイルを披露しました。これらの成績により、大谷翔平は大会MVPに輝き、その二刀流のスター性は一層評価され、知名度を高めました。                                                                                                スタイルを披露しました。これらの成績により、大谷翔平はさらに、大谷の活躍はWBCの大会全体の成功に不可欠な要素となり、大会が世界的な注目を浴びるきっかけとなりました。彼の野球選手としての卓越した才能は、野球ファンにとっても圧巻のものであり、そのキャリアは非常に注目されています。また、大谷の 
人間性も大会中に際立ち、特に決勝戦の前に行った感動的なスピーチは、チームメイトに向けた力強いメッセージとして記憶に残りました。そのスピーチは世界中で多くの言語に翻訳され、大谷選手が次に目指すのは、所属するエンゼルスで世界一になることで 間性も大会中に際立ち、特に決勝戦の前に行った感動的な
す。多くのファンがその活躍を心待ちにしています。
```
