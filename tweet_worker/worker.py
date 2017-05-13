#!/usr/bin/env python
from __future__ import print_function
import threading
import os
import time
from textblob import TextBlob
import boto3
import json
from kafka import KafkaConsumer
import json, requests
from six.moves import configparser

worker_num = 10
id = 1

end_point = 'search-jacketsu-4pm2nv7dseksmqm2v4edzc2xxe.us-east-1.es.amazonaws.com'
index = 'twitter'
mapping_type = 'tweet'  
address = 'http://%s/%s/%s' % (end_point, index, mapping_type)

def worker():

    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             group_id='my-group',
                             auto_offset_reset='largest')
    consumer.subscribe(['tweets'])
    while True:
        for message in consumer:
            msg = message.value.decode()
            msg = json.loads(msg)
            text = msg["text"]
            try:
                testimonial = TextBlob(text)
                polarity = testimonial.sentiment.polarity
                if polarity > 0:
                    emotion = "positive"
                elif polarity < 0:
                    emotion = "negative"
                else:
                    emotion = "neutral"
                print(emotion)
                
            except Exception as e:
                print("ERROR: " + str(e))
                emotion = "neutral"
                print(emotion)
            global id
            msg["sentiment"] = emotion

            upload_address = '%s/_bulk' % (address)
            data = ''
            data += '{"index": {"_id": "%s"}}\n' % id
            data += json.dumps(msg) + '\n'
            id += 1
            response = requests.put(upload_address, data=data)
            print(data)

for i in range(worker_num):
    thread = threading.Thread(target=worker, name="worker")
    thread.start()
