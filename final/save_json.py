#!/usr/bin/env python
import boto3
import botocore

def connect(bucket_name):
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False

    return exists

def delete(bucket):
    for key in bucket.objects.all():
        key.delete()
    bucket.delete()

if __name__ == "__main__":
    s3 = boto3.resource('s3')
    bucket_name = 'stocktweetbucket'

    bucket = s3.Bucket(bucket_name)

    exists = connect(bucket_name)
    print (exists)

    filename = 'stock.json'
    s3.Object(bucket_name, filename).put(Body=open(filename, 'rb'))

#        delete(bucket)
