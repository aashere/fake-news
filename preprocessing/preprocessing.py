import pandas as pd
import requests, json, re

class Preprocessor:
    log_tweet_significance = False
    tweet_log = ""

    def __init__(self, logging=False):
        if logging:
            self.log_tweet_significance = True

    def extract_tweet_ids(self):
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

    def extract_text_data(self, api_keys, threshold):
        # Load tweet ids
        fake_tweet_ids = []
        real_tweet_ids = []

        with open('data/tweet-ids/false_tweet_ids.txt', 'r', encoding='utf8') as f:
            for tweet_id in f.readlines():
                fake_tweet_ids.append(tweet_id.strip('\n\r\t\v'))

        with open('data/tweet-ids/real_tweet_ids.txt', 'r', encoding='utf8') as f:
            for tweet_id in f.readlines():
                real_tweet_ids.append(tweet_id.strip('\n\r\t\v'))

        domain = "https://api.twitter.com"
        headers = {'Authorization': 'Bearer ' + api_keys['bearer-token']}

        fake_text_data = self.__fetch_text_data(fake_tweet_ids, domain, headers, threshold)
        real_text_data = self.__fetch_text_data(real_tweet_ids, domain, headers, threshold)

        with open('data/text-data/fake_text_data.txt', 'w+', encoding='utf8') as f:
            f.write(fake_text_data)

        with open('data/text-data/real_text_data.txt', 'w+', encoding='utf8') as f:
            f.write(real_text_data)

        if self.log_tweet_significance:
            with open('log/tweet_significance_log.txt', 'w+', encoding='utf8') as f:
                f.write(self.tweet_log)

    def __fetch_text_data(self, tweet_ids, domain, headers, threshold):
        text_data = []

        for i, tweet_id in enumerate(tweet_ids):
            if i < threshold:
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