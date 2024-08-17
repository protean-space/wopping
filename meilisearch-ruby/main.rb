# frozen_string_literal: true

require 'json'
require 'meilisearch'

client = MeiliSearch::Client.new('http://localhost:7700', 'YYCZVdwe-m10pvbIHwe_pir3UEZcantuHES2yOSBfv0')

meguro_json = File.read('../opendata/data/sample.json')
data = JSON.parse(meguro_json)

client.index('meguro-data').add_documents(data)

puts meguro_json
