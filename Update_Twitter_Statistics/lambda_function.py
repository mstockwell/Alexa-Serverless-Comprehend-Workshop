import boto3
from boto3 import resource
from botocore.exceptions import ClientError
from time import gmtime, strftime
import json
import os

dynamodb = resource('dynamodb')    
twitter_stat_table = dynamodb.Table(os.environ['STATS_TABLE'])
twitter_tweet_table = dynamodb.Table(os.environ['TWEET_TABLE'])

def set_most_recent_tweet():
    try:
        response = twitter_stat_table.get_item(
            Key={'name': 'LATEST'}
    )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        response = twitter_tweet_table.get_item(
                Key={'tweetid': item['sinceid']})
        tweet = response['Item']
        twitter_stat_table.put_item(
            Item={
                'name': 'MOST RECENT',
                'tweet_text': tweet['text'],
                'sinceid': tweet['tweetid'],
                'tweet_screen_name': tweet['screen_name'],
                'last_update_datetime': tweet['created'],
                'count':0
            }   
        )

def compute_tweet_totals():
    total_count = 0
    retweet_count = 0
    favorite_count = 0
    response = twitter_tweet_table.scan()
    for i in response['Items']:
        if i['retweet_count'] >= retweet_count:
            retweet_count = i['retweet_count']
            most_retweeted = i
        if i['favorite_count'] >= favorite_count:
            favorite_count = i['favorite_count']
            most_favorited = i
        total_count +=1
    twitter_stat_table.put_item(
        Item={
            'name':'MOST RE TWEETED',
            'tweet_text': most_retweeted['text'],
            'sinceid': most_retweeted['tweetid'],
            'tweet_screen_name': most_retweeted['screen_name'],
            'last_update_datetime': most_retweeted['created'],
            'count': most_retweeted['retweet_count']
        }
    )
    twitter_stat_table.put_item(
        Item={
            'name':'MOST FAVORITED',
            'tweet_text': most_favorited['text'],
            'sinceid': most_favorited['tweetid'],
            'tweet_screen_name': most_favorited['screen_name'],
            'last_update_datetime': most_favorited['created'],
            'count': most_favorited['favorite_count']
        }
    )
    twitter_stat_table.put_item(Item={'name': 'TOTAL TWEETS', 'count':total_count})
    print('Number of Tweets= ',total_count)
    
def lambda_handler(event, context):
    set_most_recent_tweet()
    compute_tweet_totals()
    