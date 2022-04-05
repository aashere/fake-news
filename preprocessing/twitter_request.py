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

def batch_request(num_requests, rate_limit=180):
    batch_idxs = []

    num_splits = ceil(num_requests / rate_limit)

    for split in range(num_splits):
        start_idx = split*rate_limit
        if split == num_splits - 1:
            end_idx = start_idx + (num_requests % rate_limit)
        else:
            end_idx = start_idx + rate_limit
        batch_idxs.append((start_idx, end_idx))
    return batch_idxs

# Filtered means did we previously filter articles to only be in last 7 days
def query_tweets(article, filtered=False, logger=None):
    endpoint = "/2/tweets/search/recent"
    tweet_fields_args = ','.join(['text','conversation_id','geo','created_at','public_metrics','author_id'])

    # TODO: Update to v1.1 if you get Elevated access
    # Assume: queries contains dicts with id, keywords, utc timestamp
    # V2 queries only go as far back as 1 week from today

    query = article['keywords']
    if filtered:
        end_time = article['utc']
    else:
        end_time = get_end_time_timestamp()
    max_results = 100

    request_params = {
        'query': query,
        'tweet.fields': tweet_fields_args,
        'end_time': end_time,
        'max_results': max_results
    }

    r_dict = make_request(endpoint, request_params)
    if not r_dict:
        if logger:
            logger.log_query_request_failure(article['id'])
        return None

    return {'id': article['id'], 'response': r_dict}        


def __fetch_post_data(self, tweet_ids):
    request_args = ','.join(['text','conversation_id','geo','created_at','public_metrics','author_id'])

def __fetch_user_data(self, user_ids):
    # TODO: Add get followers and following
    request_args = ','.join(['username','created_at','public_metrics','location'])
def __fetch_reply_data(self, conversation_ids):
    request_args= ','.join([''])

def __fetch_text_data(self, tweet_ids, domain, headers, request_threshold):
    text_data = []

    for i, tweet_id in enumerate(tweet_ids):
        if i < request_threshold:
            # Tweet data item
            tweet_text_data = {
                'tweet_id': tweet_id,
                'tweet_text': None,
                'replies': None
            }

            # Request tweet text
            r = requests.get(domain + '/2/tweets/' + tweet_id, headers=headers)
            if r.status_code != 200:
                print('Tweet Text Request Failed for ID: {}'.format(tweet_id))
            else:
                response = json.loads(r.text)
                if 'data' in response:
                    tweet_data = response['data']
                    if 'text' in tweet_data:
                        tweet_text = tweet_data['text']
                        # Filter out urls from tweet text
                        text_list = re.split('\s',tweet_text)
                        filtered_text = ""
                        for text in text_list:
                            if 'http' not in text:
                                filtered_text += " " + text
                        tweet_text_data['tweet_text'] = filtered_text
                    else:
                        if self.log_tweet_significance:
                            self.tweet_log += tweet_id+"\n"
                else:
                    if self.log_tweet_significance:
                            self.tweet_log += tweet_id+"\n"
                
            
            # Request replies text
            # First grab conversation_id of the tweet
            r = requests.get(domain + '/2/tweets/' + tweet_id + '?tweet.fields=conversation_id', headers=headers)
            if r.status_code != 200:
                print('Tweet Conversation ID Request Failed for ID: {}'.format(tweet_id))
            else:
                response = json.loads(r.text)
                if 'data' in response:
                    response_data = response['data']
                    if 'conversation_id' in response_data:
                        conv_id = response_data['conversation_id']
                        # Then grab all tweets corresponding to this conversation
                        r = requests.get(domain + '/2/tweets/search/recent?max_results=100&query=conversation_id:' + conv_id, headers=headers)
                        if r.status_code != 200:
                            print('Tweet Replies Fetching Failed for ID: {}'.format(tweet_id))
                        else:
                            reply_list = []
                            response = json.loads(r.text)
                            if 'data' in response:
                                replies = response['data']
                                for reply in replies:
                                    reply_text = reply['text']
                                    # Filter out urls from reply text
                                    text_list = re.split('\s', reply_text)
                                    filtered_text = ""
                                    for text in text_list:
                                        if 'http' not in text:
                                            filtered_text += " " + text
                                    reply_list.append(filtered_text)
                                tweet_text_data['replies'] = reply_list
                            else:
                                if self.log_tweet_significance:
                                    self.tweet_log += tweet_id+"\n"
                    else:
                        if self.log_tweet_significance:
                            self.tweet_log += tweet_id+"\n"
                else:
                    if self.log_tweet_significance:
                            self.tweet_log += tweet_id+"\n"

        empty_fields = False
        for key in tweet_text_data.keys():
            if tweet_text_data[key] is None:
                empty_fields = True
        if empty_fields:
            continue
        else:
            text_data.append(tweet_text_data)
        
    return json.dumps(text_data)