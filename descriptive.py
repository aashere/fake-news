import json
from preprocessing.data_collection import fetch_data_query
from logger import Logger
from nlp.nlp import extract_query_data

# Logger for logging
log = Logger()

# Extract keywords from scraped data to form queries
#extract_query_data()

# Extract tweet id's into data/processed folder
#proc.extract_tweet_ids()

# TODO: Threshold querying and calculate end_time
# Get tweets by query
#fetch_data_query(logger=log)

# TODO: Get user data

# TODO: Get replies data

# TODO: Parse data out

# TODO: Analyze features

log.dump()