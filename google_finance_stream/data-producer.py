from googlefinance import getQuotes
import argparse
import logging
import json
import requests
import time
from datetime import datetime
from worker import ElasticsearchStock

id = 1
end_point = 'search-stock-aqj3tyurz5jx3mut3ot4ll7h3a.us-west-2.es.amazonaws.com'
index = 'stock'
mapping_type = 'price'  
address = 'http://%s/%s/%s' % (end_point, index, mapping_type)
upload_address = '%s/_bulk' % (address)

def upload(stock_list):
    global id
        
    data = ''
    for stock in stock_list:
        data += '{"index": {"_id": "%s"}}\n' % id
        data += json.dumps(stock) + '\n'
        id += 1

    print (data)

#    response = requests.put(upload_address, data=data)
#    print(response)

def fetch_stocks(symbols):
    stock_list = getQuotes(symbols)
    for data in stock_list:
        print (data)
    return stock_list

def save_json(es, searchkey):
    response = es.search_stock(searchkey)
    stock_json = response['hits']['hits']
    print (stock_json)

    with open('%s.json' % searchkey, 'w') as f:
        json.dump(stock_json, f)

if __name__ == '__main__':
    symbols = ['AAPL', 'GOOGL', 'FB', 'AMZN', 'LNKD', 'MSFT', 'TSLA']
    while False:
        stocks = fetch_stocks(symbols)
        upload(stocks)
        time.sleep(5)

    est = ElasticsearchStock()
    save_json(est, 'AAPL')


