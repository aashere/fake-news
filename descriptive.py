import json
from preprocessing.data_collection import get_all_user_data
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

# TODO: Analyze features

log.dump()