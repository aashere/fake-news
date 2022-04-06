import pandas as pd
import re, json, time
from data.raw.tweet_articles.tweet_likes_false import d as false_scraped
from data.raw.tweet_articles.tweet_likes_true import d as true_scraped
from preprocessing.twitter_request import batch_request, query_tweets

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

def query_raw_data(logger=None, request_threshold=None):
    # Load in article query dicts from file
    with open('data/processed/article_keywords/fake_keywords.json', 'r') as f:
        fake_articles = json.loads(f.read())

    with open('data/processed/article_keywords/true_keywords.json', 'r') as f:
        true_articles = json.loads(f.read())

    # Split queries into batches based on the rate limit
    rate_limit = 180
    fake_batches = batch_request(len(fake_articles), rate_limit=rate_limit)
    true_batches = batch_request(len(true_articles), rate_limit=rate_limit)

    with open('data/raw/twitter_data/fake_twitter_raw.json', 'w+') as f:
        f.write('[')
        for batch_idx, batch in enumerate(fake_batches):
            article_batch = fake_articles[batch[0]:batch[1]]
            for article_idx, article_dict in enumerate(article_batch):
                if request_threshold and article_idx + batch_idx*rate_limit >= request_threshold:
                    break
                response = query_tweets(article_dict, 'fake', logger=logger)
                if not response:
                    continue
                if (not request_threshold and article_idx + batch_idx*rate_limit == len(fake_articles) - 1) or (request_threshold and article_idx + batch_idx*rate_limit == request_threshold - 1):
                    f.write(response + '\n')
                else:
                    f.write(response + ',\n')
            # Sleep 15:05 min between batches
            if not request_threshold:
                time.sleep(905)
        f.write(']')

    with open('data/raw/twitter_data/real_twitter_raw.json', 'w+') as f:
        f.write('[')
        for batch_idx, batch in enumerate(true_batches):
            article_batch = true_articles[batch[0]:batch[1]]
            for article_idx, article_dict in enumerate(article_batch):
                if request_threshold and article_idx + batch_idx*rate_limit >= request_threshold:
                    break
                response = query_tweets(article_dict, 'real', logger=logger)
                if not response:
                    continue
                if (not request_threshold and article_idx + batch_idx*rate_limit == len(true_articles) - 1) or (request_threshold and article_idx + batch_idx*rate_limit == request_threshold - 1):
                    f.write(response + '\n')
                else:
                    f.write(response + ',\n')
            # Sleep 15:05 min between batches
            if not request_threshold:
                time.sleep(905)
        f.write(']')
