import json, os
import pandas as pd

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

    if type == 'fake':
        # Cleaning
        # Drop missing tweet ids
        final_df.iloc[:,0] = final_df.iloc[:,0].astype(str)
        final_df = final_df[final_df.iloc[:,0].str.match('[0-9]+', na=False)]
        final_df.iloc[:,0] = final_df.iloc[:,0].astype('int64').astype(str)

        # Fix data types
        final_df.iloc[:,1] = final_df.iloc[:,1].astype('int64').astype(str)
        final_df.iloc[:,5] = final_df.iloc[:,5].astype('int64').astype(str)

    # Drop columns with less than 50% null values
    null_cols = []
    for col in list(final_df.columns):
        if final_df.loc[:,col].isna().sum() > 0.5*final_df.shape[0]:
            null_cols.append(col)
    final_df = final_df.drop(columns=null_cols)
    
    # Write to file
    final_df.to_csv(file_paths[type]['final_write'], index=False)