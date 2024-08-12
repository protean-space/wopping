import json
import unicodedata
import fasttext
import fasttext.util
import re
import argparse

# コマンドライン引数の処理
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate related words using FastText.")
    parser.add_argument('--query', type=str, required=True, help='The query string to find related words for.')
    return parser.parse_args()

# JSONファイルの読み込み
with open('../data/opendata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# メタデータとhitsのテキスト部分を抽出する関数
def extract_text(entry):
    metadata = entry.get('metadata', {})
    hits = entry.get('hits', [])
    
    # メタデータを結合してテキスト化
    metadata_text = ' '.join([
        metadata.get('title', ''),
        metadata.get('datasetTitle', ''),
        metadata.get('datasetDesc', ''),
        metadata.get('dataTitle', ''),
        metadata.get('dataDesc', '')
    ])
    
    # hitsをJSON形式の文字列として結合し、数値や不必要な文字列をフィルタリング
    hits_texts = []
    for hit in hits:
        hit_text = json.dumps(hit, ensure_ascii=False)
        # 数値や特殊記号を除去
        hit_text = re.sub(r'\d+', '', hit_text)
        hit_text = re.sub(r'[^\w\s]', '', hit_text)
        hits_texts.append(hit_text)
    
    hits_text = ' '.join(hits_texts)
    
    # メタデータとhitsを結合して返す
    return f"{metadata_text} {hits_text}"

# データのテキストをすべて抽出し、学習用に保存
texts = []
for item in data:
    for key, entry in item.items():
        texts.append(extract_text(entry))

# 文献データをテキストファイルに保存
with open('documents.txt', 'w', encoding='utf-8') as f:
    for text in texts:
        f.write(text + '\n')

# 文献データを使用してFastTextモデルを学習
fasttext_model = fasttext.train_unsupervised('documents.txt', model='skipgram', dim=100)

# クエリの前処理関数
def preprocess_query(query):
    query = unicodedata.normalize('NFKC', query)
    return query

# FastTextモデルを使用して単語ベースの関連ワードを取得
def get_related_words(word, top_n=10):
    try:
        nearest_neighbors = fasttext_model.get_nearest_neighbors(word, k=top_n)
        # 関連度が高い単語のみをフィルタリングして返す
        related_words = []
        for similarity, neighbor_word in nearest_neighbors:
            if len(neighbor_word.split()) == 1:  # 単語レベルでの出力に限定
                related_words.append((neighbor_word, similarity))
        return related_words
    except KeyError:
        return []

# クエリから関連単語を抽出してJSON形式で出力
def generate_related_words_json(query):
    query = preprocess_query(query)
    query_terms = query.split()
    
    # 関連単語の取得とJSON形式のデータ生成
    related_words_pairs = []
    for term in query_terms:
        related_words = get_related_words(term)
        for neighbor_word, _ in related_words:
            related_words_pairs.append({"source": term, "target": neighbor_word})
    
    return related_words_pairs

def main():
    args = parse_arguments()  # コマンドライン引数をパース
    query = args.query
    related_words_pairs = generate_related_words_json(query)

    # 関連単語のJSON形式の出力
    json_output = json.dumps(related_words_pairs, ensure_ascii=False, indent=2)
    print("\n関連単語のJSON形式の出力:")
    print(json_output)

    # 必要に応じてファイルに保存
    # with open('related_words.json', 'w', encoding='utf-8') as f:
    #     f.write(json_output)

if __name__ == "__main__":
    main()
