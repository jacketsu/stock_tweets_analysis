#!/usr/bin/env python
from __future__ import print_function
import time
import tweepy
import json

from getpass import getpass
from datetime import datetime
from six.moves import configparser
from kafka import KafkaProducer
# from sets import Set

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, kafka_producer):
        tweepy.StreamListener.__init__(self)
        self.kafka_producer = kafka_producer
        self.TIMEZONE_OFFSET = datetime.utcnow() - datetime.now()

    def on_status(self, status):
        try:
            # coords = status.coordinates["coordinates"]
            local_created_time = status.created_at - self.TIMEZONE_OFFSET;
            tweet = {
                'name': status.author.screen_name,
                'time': local_created_time.strftime("%Y/%m/%d %H:%M:%S"),
                # 'location': {'lat': coords[1], 'lon': coords[0]},
                'text': status.text,
                'profile_image_url': status.author.profile_image_url,
                'sentiment': ''
            }
            # press = set(['YahooFinance','WSJ','TheEconomist','Forbes','business','MarketWatch','WSJpersfinance',
            #                 'ftfinancenews','WSJbusiness','NYIFinance','NYCCFB','FinancialTimes',
            #                 'clusterstock','wiley_finance','FortuneMagazine','ftmoney','TradeFinance','NYCFinance','FT',
            #                 'EconBizFin','ETFinance','StockTwist','DeutscheBank', 'Xiaovid'])
            # if tweet['name'] in press:
            #     # self.kafka_producer.send('tweets', json.dumps(tweet).encode('utf-8'))
            #     print('get')
            #     print(tweet)
#               print ("sending tweets to kafka")
            # print(tweet);
            self.kafka_producer.send('tweets', json.dumps(tweet).encode('utf-8'))
            # print(tweet['name'])
            print(tweet)
            
            return True

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print ('An error has occured! Status code = %s' % status_code)
        return True  # keep stream alive

    def on_timeout(self):
        print ('Snoozing Zzzzzz')


def start_stream(kafka_producer, config_filename):
    consumer_key, consumer_secret, access_token, access_token_secret = read_config(config_filename)

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    global stream
    stream = tweepy.Stream(auth, TweetStreamListener(kafka_producer), timeout=None)
    # stream.filter(languages=['en'])
    # stream.sample()
    stream.filter(track=['Google','Facebook','Apple','Amazon','Linked','Microsoft','Bloomberg',
                            'Tweet','Tesla'], languages=['en'])
    # stream.filter(track=['YahooFinance','WSJ','TheEconomist','Forbes','business','MarketWatch','WSJpersfinance',
    #                         'ftfinancenews','WSJbusiness','NYIFinance','NYCCFB','FinancialTimes',
    #                         'clusterstock','wiley_finance','FortuneMagazine','ftmoney','TradeFinance','NYCFinance','FT',
    #                         'EconBizFin','ETFinance','StockTwist','DeutscheBank', 'Xiaovid'], languages=['en'])
    # stream.filter(locations=[-180, -90, 180, 90], languages=['en'])

def stop_stream():
    print ('stopping stream...')
 #   observer.save_tweets()
    global stream
    stream.disconnect()

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config.get('TweetStreaming', 'consumer_key')
    consumer_secret = config.get('TweetStreaming', 'consumer_secret')
    access_token = config.get('TweetStreaming', 'access_token')
    access_token_secret = config.get('TweetStreaming', 'access_token_secret')

    return (consumer_key, consumer_secret, access_token, access_token_secret)


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10))
    start_stream(producer, '../setup.cfg')

