import pandas as pd
import re, json
from data.raw.tweet_articles.tweet_likes_false import d as false_scraped
from data.raw.tweet_articles.tweet_likes_true import d as true_scraped
from preprocessing.twitter_request import query_tweets

def extract_tweet_ids(self, thresholded=False, scraped=False, likes_threshold=100):
    if thresholded:
        # Load tweet ids
        fake_tweet_ids = []
        real_tweet_ids = []
        
        if scraped:
            for k, v in false_scraped.items():
                m = re.search('^[0-9]', v)
                keep = m or int(v) > likes_threshold
                if keep:
                    m = re.search('/([0-9]+)', k)
                    fake_tweet_ids.append(m.group(1))

            for k, v in true_scraped.items():
                m = re.search('^[0-9]', v)
                keep = m or int(v) > likes_threshold
                if keep:
                    m = re.search('/([0-9]+)', k)
                    real_tweet_ids.append(m.group(1))
        else:
            with open('data/tweet-ids/false_tweet_ids.txt', 'r', encoding='utf8') as f:
                for tweet_id in f.readlines():
                    fake_tweet_ids.append(tweet_id.strip('\n\r\t\v'))

            with open('data/tweet-ids/real_tweet_ids.txt', 'r', encoding='utf8') as f:
                for tweet_id in f.readlines():
                    real_tweet_ids.append(tweet_id.strip('\n\r\t\v'))

        for tweet_id in fake_tweet_ids:
            try:
                int(tweet_id)
            except(ValueError):
                print("Fake Tweet IDs parsed incorrectly.")
        for tweet_id in real_tweet_ids:
            try:
                int(tweet_id)
            except(ValueError):
                print("Real Tweet IDs parsed incorrectly.")
    else:
        false_cols = ['label','politifact_url','annotation','archive_url','twitter_url','tweet_id']
        real_cols = ['politifact_url','annotation','archive_url','twitter_url','tweet_id']

        # Load raw data
        fake_data = pd.read_csv('data/raw/politifact_false.csv', names=false_cols, header=None, encoding='utf8')
        real_data = pd.read_csv('data/raw/politifact_true.csv', names=real_cols, header=None, encoding='utf8')

        # Only consider rows where we have tweet id
        fake_data = fake_data[fake_data['tweet_id'].notna()]
        real_data = real_data[real_data['tweet_id'].notna()]

        fake_data = fake_data[fake_data['tweet_id'].str.contains('[0-9]+')]
        real_data = real_data[real_data['tweet_id'].str.contains('[0-9]+')]

        # Extract tweet id column
        fake_data_ids = fake_data['tweet_id']
        real_data_ids = real_data['tweet_id']

        # Save to tweet-ids folder
        fake_data_ids.to_csv('data/tweet-ids/false_tweet_ids.txt', header=None, index=None, sep='\n', encoding='utf8')
        real_data_ids.to_csv('data/tweet-ids/real_tweet_ids.txt', header=None, index=None, sep='\n', encoding='utf8')

def fetch_data_query(logger=None, request_threshold=None):
    # Load in article query dicts from file
    with open('data/processed/article_keywords/fake_keywords.json', 'r') as f:
        fake_articles = json.loads(f.read())

    with open('data/processed/article_keywords/true_keywords.json', 'r') as f:
        true_articles = json.loads(f.read())
    
    fake_responses = []
    for article_dict in fake_articles:
        fake_responses.append(query_tweets(article_dict, logger=logger))
        
    true_responses = []
    for article_dict in true_articles:
        true_responses.append(query_tweets(article_dict, logger=logger))

    # Write query response data to file
    with open('data/processed/twitter_data/raw_response/fake_query_response.json', 'w+') as f:
        f.write(json.dumps(fake_responses))

    with open('data/processed/twitter_data/raw_response/true_query_response.json', 'w+') as f:
        f.write(json.dumps(true_responses))
