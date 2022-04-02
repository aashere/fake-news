import json
from preprocessing.preprocessing import Preprocessor

# Load API keys from file
api_keys = dict()

with open('api-keys/api_keys_ameya.txt', 'r') as f:
    api_keys = json.loads(f.read())

# TODO: Edit preprocessing to maximize info returned in one request
proc = Preprocessor(logging=False)

# Extract tweet id's into data/processed folder
#proc.extract_tweet_ids()

# Get text from API
#proc.extract_text_data(api_keys, 30)

# TODO: Get metrics from API

# TODO: Get graph data from API