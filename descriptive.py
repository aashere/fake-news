import json
from preprocessing.preprocessing import extract_tweet_ids, extract_text_data

# Load API keys from file
api_keys = dict()

with open('api-keys/api_keys_ameya.txt', 'r') as f:
    api_keys = json.loads(f.read())

# TODO: Edit preprocessing to maximize info returned in one request

# Extract tweet id's into data/processed folder
#extract_tweet_ids()

# Get text from API
#extract_text_data(api_keys, 30)

# TODO: Get metrics from API

# TODO: Get graph data from API