# - connect to any kafka broker
# - fetch stock price every second
from googlefinance import getQuotes
from kafka import KafkaProducer
from kafka.errors import KafkaError
import argparse
import logging
import json
import requests
import time
from datetime import datetime

import schedule
import atexit
import worker

# - logging config
logging.basicConfig()
logger = logging.getLogger('data-producer')
# - debug, info, warning, error
logger.setLevel(logging.DEBUG)
symbol = 'AAPL'
symbol2='GOOGL'
kafka_broker = '192.168.99.100:9092'
topic = 'bigdata'

id=1
end_point = 'search-stock-aqj3tyurz5jx3mut3ot4ll7h3a.us-west-2.es.amazonaws.com'
index = 'stock'
mapping_type = 'price'  
address = 'http://%s/%s/%s' % (end_point, index, mapping_type)
upload_address = '%s/_bulk' % (address)

def upload(data1):
        

       

        global id

        
        data = ''
        data += '{"index": {"_id": "%s"}}\n' % id
        data += json.dumps(data1) + '\n'
        id += 1
        print ('upload')
        print(data)
        response = requests.put(upload_address, data=data)
        print(response)
        




def fetch_price(producer, symbol):
    logger.debug('start to fetch price for %s' % symbol)
    raw = getQuotes(symbol)
    price = json.dumps(raw)
    # price1=[
    # {
    #     # "Index": "NASDAQ",
    #     # "LastTradeWithCurrency": "153.74",
    #     # "LastTradeDateTime": "2017-05-09T14:50:15Z",
    #     #"LastTradePrice": "153.74",
    #     # "LastTradeTime": "2:50PM EDT",
    #     # "LastTradeDateTimeLong": "May 9, 2:50PM EDT",
    #     # "StockSymbol": "AAPL",
    #     "ID": "22144"
#     # }
# ]
     
    #producer.send(topic=topic, value=json.dumps(price).encode('utf-8'), timestamp_ms=time.time())
    upload(raw[0])
    logger.debug('sent stock price for %s, price is %s' % (symbol,raw[0]))

def shut_down(producer):
    logger.debug('exiting program')
    producer.flush(10)
    producer.close()
    logger.debug('kafka producer closed, exiting')  

def fetch_a_stock(producer,symbol):
    schedule.every(1).second.do(fetch_price, producer, symbol)

if __name__ == '__main__':
   

    # - instantiate kafka producer
    producer = KafkaProducer(bootstrap_servers=kafka_broker, api_version=(0,10))
    #start_stream(producer, '../setup.cfg')

    #schedule.every(1).second.do(fetch_price, producer, symbol)##aapl
    #schedule.every(1).second.do(fetch_price, producer, symbol2)##google
    fetch_a_stock(producer,'AAPL')
    fetch_a_stock(producer,'GOOGL')
    fetch_a_stock(producer,'FB')
    fetch_a_stock(producer,'AMZN')
    fetch_a_stock(producer,'LNKD')
    fetch_a_stock(producer,'MSFT')
    fetch_a_stock(producer,'TSLA')




    #send json to topic every 5 seconds
    atexit.register(shut_down, producer)
    while True:
        schedule.run_pending()

        time.sleep(5)