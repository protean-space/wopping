import json
import unicodedata
import argparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# コマンドライン引数の処理
def parse_arguments():
    parser = argparse.ArgumentParser(description="Search documents using TF-IDF.")
    parser.add_argument('--query', type=str, required=True, help='The query string to search for.')
    return parser.parse_args()

# JSONファイルの読み込み
with open('../slm/data/opendata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# メタデータのテキスト部分を抽出する関数
def extract_text(entry):
    metadata = entry.get('metadata', {})
    return ' '.join([
        metadata.get('title', ''),
        metadata.get('datasetTitle', ''),
        metadata.get('datasetDesc', ''),
        metadata.get('dataTitle', ''),
        metadata.get('dataDesc', '')
    ])

# データのテキストをすべて抽出
texts = []
for item in data:
    for key, entry in item.items():
        texts.append(extract_text(entry))

# TF-IDFベクトライザーの初期化
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),     # ユニグラムとバイグラムを使用
    max_df=0.85,            # 上位85%の頻度の単語を無視
    min_df=2,               # 2つ以上の文書に登場する単語のみを考慮
    stop_words=['の', 'に', 'を', 'は'],  # カスタムストップワードのリスト
    sublinear_tf=True       # サブリニアTFスケーリングを有効化
)

# テキストデータのフィッティングとベクトル化
tfidf_matrix = vectorizer.fit_transform(texts)

# クエリの前処理関数
def preprocess_query(query):
    # 全角・半角の統一
    query = unicodedata.normalize('NFKC', query)
    return query

# クエリを部分文字列検索する関数
def partial_match_search(query):
    matches = []
    for idx, text in enumerate(texts):
        if query in text:
            matches.append(idx)
    return matches

# 複数の単語に対する部分一致検索と結合
def multi_term_search(terms):
    combined_results = []
    for term in terms:
        partial_matches = partial_match_search(term)
        if partial_matches:
            for index in partial_matches:
                query_vec = vectorizer.transform([texts[index]])
                cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
                score = cosine_similarities[index]
                result = {
                    'score': score,
                    'metadata': list(data[index].values())[0]['metadata']
                }
                combined_results.append(result)
    return combined_results

# 複合検索の処理
def search(query, top_n=5):
    # クエリの前処理
    query = preprocess_query(query)

    # クエリを分割
    query_terms = query.split()

    combined_results = multi_term_search(query_terms)

    # クエリ全体での検索を実行
    query_vec = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
    related_docs_indices = cosine_similarities.argsort()[-top_n:][::-1]

    for index in related_docs_indices:
        score = cosine_similarities[index]
        if score > 0.0:
            result = {
                'score': score,
                'metadata': list(data[index].values())[0]['metadata']
            }
            combined_results.append(result)

    # スコアで結果をソート
    combined_results.sort(key=lambda x: x['score'], reverse=True)

    # 重複を避けるために、上位n件の結果を返す
    seen_titles = set()
    unique_results = []
    for result in combined_results:
        title = result['metadata'].get('title', 'N/A')
        if title not in seen_titles:
            seen_titles.add(title)
            unique_results.append(result)
        if len(unique_results) >= top_n:
            break

    return unique_results

def main(query):
    # args = parse_arguments()  # コマンドライン引数をパース
    # query = args.query
    results = search(query)

    # 結果の表示
    json_array = []
    for result in results:
        # datasetIdが 存在しない場合: None, 存在する場合: ウェブページ上のURLに変換
        url = None if result['metadata'].get('datasetId') is None else f"https://catalog.data.metro.tokyo.lg.jp/dataset/{result['metadata'].get('datasetId')}"

        json_array.append({
            "title": result['metadata'].get('title'),
            "url": url,
            "description": result['metadata'].get('dataDesc')
        })

    return json.dumps(json_array, ensure_ascii=False)
