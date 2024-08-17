import meilisearch
import json

client = meilisearch.Client('http://localhost:7700', 'QtcbkGgDs5SnOtTTzzgafR_S8eQoQCo5MAmhUfuXQkI')

json_file = open('movies.json', encoding='utf-8')
movies = json.load(json_file)
client.index('meguro-data').add_documents(movies)
