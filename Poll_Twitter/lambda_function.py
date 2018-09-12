import boto3
from boto3 import resource
from time import gmtime, strftime
import json
import os
import tweepy
from tweepy import OAuthHandler

# Create AWS Sessions and DynamoDB resources
session = boto3.Session()
dynamodb_resource = resource('dynamodb')
twitter_state_table = dynamodb_resource.Table(os.environ['STATS_TABLE'])
tweet_table = dynamodb_resource.Table(os.environ['TWEET_TABLE'])

def get_secret():
    secret_name = os.environ['SECRETNAME']
    region_name = os.environ['SECRETREGION']
    endpoint_url = os.environ['SECRETENDPOINT']
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        endpoint_url=endpoint_url
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    jsonsecret = json.loads(secret)
    return (jsonsecret['consumer_key'], jsonsecret['consumer_secret'], jsonsecret['access_token'], jsonsecret['access_token_secret'])

def lambda_handler(event, context):
    search_text = os.environ['SEARCH_TEXT']
    print(search_text)
    response = twitter_state_table.get_item(Key={'name': 'LATEST'})
    sinceid = int(response['Item']['sinceid'])
    max_tweets = 1000
    tweet_count = 0
    consumerkey, consumersecret, accesstoken, accesstokensecret = get_secret()
    
    # Set up OAuth and integrate with API
    auth = tweepy.OAuthHandler(consumerkey, consumersecret)
    auth.set_access_token(accesstoken, accesstokensecret)
    api = tweepy.API(auth)
    
    for tweet in tweepy.Cursor(api.search, q=search_text, result_type="recent", since_id=sinceid, include_entities=False, count=100).items(max_tweets):
        print(tweet.id)
        response = tweet_table.put_item(
            Item={
                'tweetid': tweet.id,
                'text': tweet.text,
                'created': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'screen_name': tweet.user.screen_name,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count
            }   
        )
        tweet_count += 1
        if sinceid < tweet.id:
            sinceid = tweet.id

    if (tweet_count == 0):
        print('no tweets')
    else:
        print('tweets')
        twitter_state_table.put_item(Item={'name': 'LATEST', 'sinceid': sinceid, 'last_update_datetime': strftime("%Y-%m-%d %H:%M:%S", gmtime())})
