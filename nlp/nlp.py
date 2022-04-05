import pandas as pd
import json, re
from preprocessing.utils import article_time_to_utc, get_end_time_timestamp, is_timestamp_in_range

def remove_stop_words(x, stop_words):
    cleaned = re.sub('\u2018','\'', x)
    cleaned = re.sub('\u2019','\'', cleaned)
    cleaned = re.sub('\u201c','\'', cleaned)
    cleaned = re.sub('\u201d','\'', cleaned)
    cleaned = re.sub('[!#$%&()*+,.:;<=>?@[\]^_`{|}~\"\'/]', '', cleaned)
    cleaned = cleaned.split(' ')
    res = []
    for word in cleaned:
        if word not in stop_words:
            res.append(word)
    return ' '.join(res)

def extract_query_data(filter=False):
    # Load stop words into dict
    stop_words = dict()

    with open('nlp/stop_words/extra_stop.txt', 'r', encoding='utf8') as f:
        for word in f.readlines():
            stop_word = word.strip('\n')
            if stop_word not in stop_words:
                stop_words[stop_word] = 1

    with open('nlp/stop_words/stop_words_english.txt', 'r', encoding='utf8') as f:
        for word in f.readlines():
            stop_word = word.strip('\n')
            if stop_word not in stop_words:
                stop_words[stop_word] = 1

    # Load article data into dataframe
    fake_df = pd.read_csv('data/raw/all_articles/politifact_statements_false.csv', index_col=0, encoding='utf8')
    true_df = pd.read_csv('data/raw/all_articles/politifact_statements_true.csv', index_col=0, encoding='utf8')

    # Just get the columns we need:
    fake_df = fake_df[['Statement','Date']]
    true_df = true_df[['Statement', 'Date']]

    fake_df['Statement'] = fake_df['Statement'].str.lower()
    true_df['Statement'] = true_df['Statement'].str.lower()

    # Add keywords as new column
    fake_df['keywords'] = fake_df['Statement'].apply(lambda x: remove_stop_words(x, stop_words))
    true_df['keywords'] = true_df['Statement'].apply(lambda x: remove_stop_words(x, stop_words))

    # Add new columns with UTC Timestamp
    fake_df['utc'] = fake_df['Date'].apply(lambda x: article_time_to_utc(x))
    true_df['utc'] = true_df['Date'].apply(lambda x: article_time_to_utc(x))

    if filter:
        # Get end_time timestamp
        end_time = get_end_time_timestamp()

        # Filter out articles before this timestamp
        fake_in_range = fake_df['utc'].apply(lambda x: is_timestamp_in_range(x, end_time))
        fake_df = fake_df[fake_in_range]

        # Filter out articles before this timestamp
        true_in_range = true_df['utc'].apply(lambda x: is_timestamp_in_range(x, end_time))
        true_df = true_df[true_in_range]

    # Write id, keywords, date to file
    fake_df = fake_df.reset_index().rename(columns={'index': 'id'})
    true_df = true_df.reset_index().rename(columns={'index': 'id'})

    fake_res = fake_df[['id','keywords','utc']]
    true_res = true_df[['id','keywords','utc']]

    fake_res.to_json('data/processed/article_keywords/fake_keywords.json', orient='records')
    true_res.to_json('data/processed/article_keywords/true_keywords.json', orient='records')