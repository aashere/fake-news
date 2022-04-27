import json, os
import pandas as pd
from log_func.logger import Logger

#from nlp.nlp import extract_query_data

# TODO: Make setup.py for distribution

# Logger for logging
log = Logger()

# Extract keywords from scraped data to form queries
#extract_query_data()

# Extract tweet id's into data/processed folder
#proc.extract_tweet_ids()

# Get tweets by query
#query_tweets(logger=log)

# Get user data, parse
#get_all_user_data()

# TODO: Get graph data, parse

# Join everything into one dataset
file_paths = {
    'fake': {
        'twitter_data_read': 'data/raw/tweet_scrape/false_tweets_raw/',
        'user_data_read': 'data/raw/user_data/fake_user_data.csv',
        'final_write': 'data/processed/full_dataset/fake_dataset.csv'
    },
    'real': {
        'twitter_data_read': 'data/raw/tweet_scrape/true_tweets_raw/',
        'user_data_read': 'data/raw/user_data/real_user_data.csv',
        'final_write': 'data/processed/full_dataset/real_dataset.csv'
    }
}

for type in ['fake', 'real']:

    # Get Twitter data and join it together
    df_list = []

    for file in os.listdir(os.path.join(file_paths[type]['twitter_data_read'])):
        if file.endswith(".csv"):
            df_list.append(pd.read_csv(file_paths[type]['twitter_data_read'] + file, encoding='utf8'))

    twitter_df = pd.concat(df_list)

    # Get User data
    user_df = pd.read_csv(file_paths[type]['user_data_read'], encoding='utf8')

    # Cleaning step
    user_df = user_df[user_df['user_id'] != 'user_id']
    twitter_df['user_id'] = twitter_df['user_id'].astype('object')

    # Join datasets together
    final_df = pd.merge(twitter_df, user_df, on='user_id', how='left')
    
    # Write to file
    final_df.to_csv(file_paths[type]['final_write'], index=False)

# TODO: Analyze features

log.dump()