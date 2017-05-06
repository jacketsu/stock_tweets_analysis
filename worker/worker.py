#!/usr/bin/env python
from __future__ import print_function
import threading
import os
import time
from textblob import TextBlob
import boto3
import json
from kafka import KafkaConsumer

# sns = boto3.client('sns', region_name='us-east-1')
# arn = 'arn:aws:sns:us-east-1:16425093:sns'
worker_num = 10

def worker():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             group_id='my-group',
                             auto_offset_reset='smallest')
    consumer.subscribe(['tweets'])
    while True:
        for message in consumer:
            msg = message.value.decode()
            msg = json.loads(msg)
            text = msg["text"]
            try:
                testimonial = TextBlob(text)
                polarity = testimonial.sentiment.polarity
                if polarity > 0.2:
                    emotion = "positive"
                elif polarity < -0.2:
                    emotion = "negative"
                else:
                    emotion = "neutral"
                # res = natural_language_understanding.analyze(text=text, features=[features.Sentiment()])
                # emotion = (json.dumps(res['sentiment']['document']['label'], indent=2))
                print(emotion)
                
            except Exception as e:
                print("ERROR: " + str(e))
                emotion = "neutral"
                print(emotion)
                
            # msg["sentiment"] = emotion
            # sns_msg = json.dumps({"default":json.dumps(msg)})
            # sns.publish(TargetArn=arn, MessageStructure='json', Message=sns_msg)
            # print(msg)



for i in range(worker_num):
    thread = threading.Thread(target=worker, name="worker")
    thread.start()
