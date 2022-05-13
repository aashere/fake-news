import requests
import json

# Load API keys from file
api_keys = dict()

with open('../api-keys.txt', 'r') as f:
    api_keys = json.loads(f.read())

# Load list of tweet ids from file
tweet_ids = list()

with open('data/tweet-ids.txt', 'r') as f:
    for id in f.readlines():
        tweet_ids.append(id.strip('\n\r\t\v'))

domain = "https://api.twitter.com"
headers = {'Authorization': 'Bearer ' + api_keys['bearer-token']}
tweet = tweet_ids[0]

# Get retweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/retweets/api-reference/get-tweets-id-retweeted_by
r = requests.get(domain + '/2/tweets/' + tweet + '/retweeted_by', headers=headers)
print("Retweets:")
print(r.text + '\n')

# Get quote tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/quote-tweets/api-reference/get-tweets-id-quote_tweets
r = requests.get(domain + '/2/tweets/' + tweet + '/quote_tweets', headers=headers)
print("Quote Tweets:")
print(r.text + '\n')

# Get replies
# First grab conversation_id of the tweet
# https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/api-reference/get-tweets-id
# https://developer.twitter.com/en/docs/twitter-api/conversation-id
r = requests.get(domain + '/2/tweets/' + tweet + '?tweet.fields=conversation_id', headers=headers)
conv_id = json.loads(r.text)['data']['conversation_id']

# Then grab all tweets corresponding to this conversation
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
# ALL TWEETS ACCESS only for Academic Research tier (https://developer.twitter.com/en/products/twitter-api/academic-research)
#r = requests.get(domain + '/2/tweets/search/all?query=conversation_id:' + conv_id, headers=headers)
# For now, we can use Recent Tweets
r = requests.get(domain + '/2/tweets/search/recent?query=conversation_id:' + conv_id, headers=headers)
print('Replies:')
print(r.text)