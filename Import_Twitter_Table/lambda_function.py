import boto3
from boto3 import resource
from boto3 import s3
from botocore.exceptions import ClientError
from time import gmtime, strftime
import simplejson as json
import decimal
import os
import random

dynamodb = resource('dynamodb')    
twitter_tweet_table = dynamodb.Table(os.environ['TWEET_TABLE'])
twitter_stat_table = dynamodb.Table(os.environ['STATS_TABLE'])
json_import_file = os.environ['JSON_IMPORT_FILE_NAME']
since_id = os.environ['SINCEID']

def lambda_handler(event, context):
    for line in open(json_import_file, 'r'):
        tweet_record = json.loads(line, parse_float = decimal.Decimal)
        twitter_tweet_table.put_item(
            Item={
                'tweetid': tweet_record['tweetid'],
                'text': tweet_record['text'],
                'created': tweet_record['created'],
                'screen_name': tweet_record['screen_name'],
                'retweet_count': tweet_record['retweet_count'],
                'favorite_count': tweet_record['favorite_count']
            }   
        )
    twitter_stat_table.put_item(Item={'name':'LATEST','sinceid':since_id})