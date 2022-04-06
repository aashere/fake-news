import json
from preprocessing.data_collection import query_raw_data
from preprocessing.parsing import parse_query_data
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
query_raw_data(logger=log, request_threshold=10)

# Parse out raw query data
parse_query_data()

# TODO: Get replies data, parse

# TODO: Get graph data, parse

# TODO: Analyze features

log.dump()