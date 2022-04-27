import requests, json, re
from preprocessing.utils import get_end_time_timestamp
from math import ceil

domain = "https://api.twitter.com"
headers = {'Authorization': None}

# Load API keys from file
api_keys = dict()

with open('api-keys/api_keys_ameya.txt', 'r') as f:
    api_keys = json.loads(f.read())

headers['Authorization'] = 'Bearer ' + api_keys['bearer-token']

def make_request(endpoint, request_params):
    request_param_string = "?"

    for k, v in request_params.items():
        request_param_string += str(k) + "=" + str(v) + "&"

    r = requests.get(domain + endpoint + request_param_string, headers=headers)
    if r.status_code != 200:
        return None
    else:
        return json.loads(r.text)

def batch_request(num_ids, rate_limit=180, request_limit = 1):
    batch_idxs = []
    num_ids_per_batch = rate_limit*request_limit

    num_splits = ceil(num_ids / num_ids_per_batch)

    for split in range(num_splits):
        start_idx = split*num_ids_per_batch
        if split == num_splits - 1:
            end_idx = start_idx + (num_ids % num_ids_per_batch)
        else:
            end_idx = start_idx + num_ids_per_batch
        batch_idxs.append((start_idx, end_idx))
    return batch_idxs

# Filtered means did we previously filter articles to only be in last 7 days
def query_tweets(article, type, filtered=False, logger=None, max_results=100):
    endpoint = "/1.1/search/tweets.json"
    tweet_fields_args = ','.join(['text','conversation_id','geo','created_at','public_metrics','author_id'])
    user_fields_args = ','.join(['username','created_at','public_metrics','location'])

    # TODO: Update to v1.1 if you get Elevated access
    # Assume: queries contains dicts with id, keywords, utc timestamp
    # V2 queries only go as far back as 1 week from today

    # Exclude retweets and quote tweets
    query = article['keywords'] + ' -is:retweet -is:quote'
    if filtered:
        end_time = article['utc']
    else:
        end_time = get_end_time_timestamp()
    max_results = max_results

    request_params = {
        'query': query,
        'tweet.fields': tweet_fields_args,
        'user.fields': user_fields_args,
        'end_time': end_time,
        'max_results': max_results,
        'expansions': 'author_id'
    }

    r_dict = make_request(endpoint, request_params)
    if not r_dict:
        if logger:
            logger.log_query_request_failure(str(article['id']) + ' ' + type)
        return None

    return json.dumps({'id': article['id'], 'response': r_dict})  

def fetch_user_data(user_ids):
    endpoint = "/2/users"
    user_fields_args = ','.join(['created_at','public_metrics','location'])

    request_params = {
        'ids': user_ids,
        'user.fields': user_fields_args,
    }

    r_dict = make_request(endpoint, request_params)
    if not r_dict:
        return None

    return {'response': r_dict}      

def fetch_graph_data(self, user_id):
    pass