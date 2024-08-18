from fastapi import FastAPI
import score

description = """
このAPIは [東京都オープンデータカタログサイト](https://portal.data.metro.tokyo.lg.jp/) にて公開されているデータを用いて、検索単語から関連するリンクを抽出します。
"""

app = FastAPI(
    title="Wopping API",
    description=description
)

@app.get("/")
async def root():
    return score.main("目黒区")
