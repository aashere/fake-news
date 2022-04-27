import pandas as pd
import re, json, time, os
from math import ceil
from data.raw.tweet_articles.tweet_likes_false import d as false_scraped
from data.raw.tweet_articles.tweet_likes_true import d as true_scraped
from preprocessing.twitter_request import batch_request, query_tweets, fetch_user_data
from preprocessing.parsing import parse_query, parse_user_response

def extract_tweet_ids(thresholded=False, scraped=False, likes_threshold=100):
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

def query_twitter(logger=None, request_threshold=None, max_results=100):
    article_args = {
        'fake': {
            'read_path': 'data/processed/article_keywords/fake_keywords.json',
            'write_path': 'data/raw/twitter_data/fake_twitter_raw.csv'
        },
        'real': {
            'read_path': 'data/processed/article_keywords/true_keywords.json',
            'write_path': 'data/raw/twitter_data/real_twitter_raw.csv'
        }
    }

    for type in ['fake', 'real']:
        # Load in article query dicts from file
        with open(article_args[type]['read_path'], 'r') as f:
            articles = json.loads(f.read())

        # Split queries into batches based on the rate limit
        rate_limit = 180
        batches = batch_request(len(articles), rate_limit=rate_limit)

        with open(article_args[type]['write_path'], 'w+') as f:
            f.write('[')
            for batch_idx, batch in enumerate(batches):
                article_batch = articles[batch[0]:batch[1]]
                for article_idx, article_dict in enumerate(article_batch):
                    if request_threshold and article_idx + batch_idx*rate_limit >= request_threshold:
                        break
                    response = query_tweets(article_dict, type, logger=logger, max_results=max_results)
                    if not response:
                        continue
                    parsed_response = parse_query(response).to_csv(index=False)
                    f.write(parsed_response)
                # Sleep 15:05 min between batches
                if not request_threshold:
                    time.sleep(905)
            f.write(']')

def get_all_user_data(request_threshold=None):
    data_args = {
        'fake': {
            'read_path': 'data/raw/tweet_scrape/false_tweets_raw/',
            'write_path': 'data/raw/user_data/fake_user_data.csv'
        },
        'real': {
            'read_path': 'data/raw/tweet_scrape/true_tweets_raw/',
            'write_path': 'data/raw/user_data/real_user_data.csv'
        }
    }

    for type in ['fake', 'real']:
        df_list = []

        for file in os.listdir(os.path.join(data_args[type]['read_path'])):
            if file.endswith(".csv"):
                df_list.append(pd.read_csv(data_args[type]['read_path'] + file, encoding='utf8'))

        df = pd.concat(df_list)
    
        user_ids = df['user_id'].drop_duplicates().astype(str).tolist()

        # Split queries into batches based on the rate limit and request limit
        rate_limit = 900
        request_limit = 100
        batches = batch_request(len(user_ids), rate_limit=rate_limit, request_limit=request_limit)

        with open(data_args[type]['write_path'], 'w+', encoding='utf8') as f:
            for batch_idx, batch in enumerate(batches):
                user_batch = user_ids[batch[0]:batch[1]]

                # Split the batch into groups of request_limit size
                request_groups = batch_request(len(user_batch), rate_limit = request_limit)
                for group_idx, group in enumerate(request_groups):
                    # Join them all into a comma separated list
                    group_user_ids = ""
                    group_user_ids = ','.join(user_batch[group[0]:group[1]])
                    if request_threshold and group_idx + batch_idx*rate_limit >= request_threshold:
                        break
                    response = fetch_user_data(group_user_ids)
                    if not response:
                        continue
                    parsed_response = parse_user_response(response).to_csv(index=False)
                    f.write(parsed_response)
                # Sleep 15:05 min between batches
                if not request_threshold:
                    time.sleep(905)