import pandas as pd
import re

file_paths = {
    'fake': {
        'read': 'data/processed/full_dataset/fake_dataset.csv'
    },
    'real': {
        'read': 'data/processed/full_dataset/real_dataset.csv'
    }
}

for type in ['fake', 'real']:
    # Read in the dataset
    df = pd.read_csv(file_paths[type]['read'], encoding='utf8')
    