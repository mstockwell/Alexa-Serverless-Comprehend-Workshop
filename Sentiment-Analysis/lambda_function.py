import boto3
from boto3 import resource
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import os
import json
import datetime

comprehend_client = boto3.client('comprehend')
dynamodb = resource('dynamodb')    
twitter_stat_table = dynamodb.Table(os.environ['STATS_TABLE'])
twitter_tweet_table = dynamodb.Table(os.environ['TWEET_TABLE'])
current_date = datetime.datetime.now().strftime ("%Y-%m-%d")


def lambda_handler(event, context):
    
    try:
        response = twitter_tweet_table.scan(FilterExpression=Attr('created').begins_with(current_date))
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        POSITIVE = 0
        NEGATIVE = 0
        NEUTRAL = 0
        MIXED = 0
        
        for i in response['Items']:
            response = comprehend_client.detect_sentiment(Text=i['text'], LanguageCode='en')
            if response['Sentiment'] == 'POSITIVE':
                    POSITIVE +=1
            elif response['Sentiment'] == 'NEGATIVE':
                    NEGATIVE +=1
            elif response['Sentiment'] == 'NEUTRAL':
                    NEUTRAL +=1    
            elif response['Sentiment'] == 'MIXED':
                    MIXED +=1
        print ("POSITIVE = ", POSITIVE)
        print ("NEGATIVE = ", NEGATIVE)
        print ("NEUTRAL = ", NEUTRAL)
        print ("MIXED = ", MIXED)
        
        twitter_stat_table.put_item(
            Item={
            'name':'SENTIMENT',
            'POSITIVE': POSITIVE,
            'NEGATIVE': NEGATIVE,
            'NEUTRAL': NEUTRAL,
            'MIXED': MIXED
            }
            )