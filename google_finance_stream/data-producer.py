from googlefinance import getQuotes
from kafka import KafkaProducer
from kafka.errors import KafkaError
import argparse
import logging
import json
import time
import schedule
import atexit
logging.basicConfig()
logger = logging.getLogger('data-producer')
logger.setLevel(logging.DEBUG)
symbol = 'AAPL'
kafka_broker = '127.0.0.1:9092'
topic = 'bigdata'

def fetch_price(producer, symbol):
    logger.debug('start to fetch price for %s' % symbol)
    price = json.dumps(getQuotes(symbol))
    producer.send(topic=topic, value=price, timestamp_ms=time.time())
    logger.debug('sent stock price for %s, price is %s' % (symbol, price))

def shut_down(producer):
    logger.debug('exiting program')
    producer.flush(10)
    producer.close()
    logger.debug('kafka producer closed, exiting')    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol', help = 'the stock symbol, such as AAPL')
    parser.add_argument('kafka_broker', help = 'the location of kafka broker')
    parser.add_argument('topic', help = 'the kafka topic to write to')
    args = parser.parse_args()
    symbol = args.symbol
    topic = args.topic
    kafka_broker = args.kafka_broker
    producer = KafkaProducer(
            bootstrap_servers=kafka_broker
        )
    
    schedule.every(30).second.do(fetch_price, producer, symbol)
    atexit.register(shut_down, producer)
    while True:

        schedule.run_pending()

        time.sleep(1)