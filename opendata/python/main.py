import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# ベースURL
base_url = "https://spec.api.metro.tokyo.lg.jp"

# 検索結果ページのURL: 最後のpageを変更すること
search_url = "https://spec.api.metro.tokyo.lg.jp/spec/search?q=%E7%9B%AE%E9%BB%92%E5%8C%BA&sort=metadata_modified_desc&page=1"

# 検索結果ページのコンテンツを取得
response = requests.get(search_url)
soup = BeautifulSoup(response.text, 'html.parser')

# データセットのリンクを取得
links = soup.find_all('a', href=True)

# ダウンロード先フォルダを作成
output_dir = 'outputjson'
os.makedirs(output_dir, exist_ok=True)

# リンクごとにデータを取得
for link in links:
    relative_url = link['href']
    
    # URLが「/spec/t」で始まるか確認
    if relative_url.startswith('/spec/t'):
        # URLのベース部分を変換し、最後に "/json" を付ける
        service_url = relative_url.replace("/spec/", "/api/")
        dataset_url = urljoin("https://service.api.metro.tokyo.lg.jp", service_url) + '/json'
        
        # POSTリクエストのヘッダーとデータ
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {}  # 空のJSONデータを送信
        
        # データをPOSTリクエストで取得
        data_response = requests.post(dataset_url, headers=headers, json=data)
        
        # 正常にデータを取得できた場合のみ処理
        if data_response.status_code == 200:
            data = data_response.json()  # JSONデータを取得
            
            # ファイル名を生成（URLの一部を使用）
            filename = relative_url.split('/')[-1] + '.json'
            filepath = os.path.join(output_dir, filename)
            
            # JSONファイルとして保存
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            print(f"データを {filepath} に保存しました。")
        else:
            print(f"データの取得に失敗しました: {dataset_url} (ステータスコード: {data_response.status_code})")

print("すべてのデータのダウンロードとJSON保存が完了しました。")
