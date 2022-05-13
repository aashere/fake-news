# Fake News Classification Project
#### Ameya Shere, Avery Greenberg, and Steve Zhao

In this project, we attempt to classify misinformation on Twitter. After achieving limited results with models that classify at the Tweet level, we develop a context-based heuristic that can classify subtopics as True or False. This heuristic could be used to improve the performance of more general classification models in this domain.

## Directory Structure
This codebase is structured as follows:
- `clustering` contains notebooks used to cluster the fake and real PolitiFact headlines and obtain topics
- `data` contains the data for the project
    - `processed` contains the full, joined dataset for all 13 COVID vaccine subtopics, as well as the same dataset with selected features, used in the modling
    - `raw` contains the raw data for the project
        - `all_articles` contains scraped PolitiFact data for all types of PolitiFact articles
        - `tweet_articles` contains scraped PolitiFact data specifically for Tweet-based articles
        - `tweet_scrape` contains scraped Twitter data for each subtopic
        - `user_data` contains user data fetched from the Twitter API for each user ID from the data contained in `tweet_scrape`
- `eda` contains notebooks for descriptive analytics for PolitiFact headline text and for Tweet and user features
- `log` contains the logging output for the preprocessing code
- `log_func` contains the code to generate logging output
- `preprocessing` contains preprocessing code for the project
    - `data_collection.py` organizes Twitter API requests for user data, batched to fit within API rate limits
    - `join.py` joins the subtopic datasets together
    - `parsing.py` parses the response from the Twitter API
    - `politifact_html_cleaning.py` cleans the PolitiFact scraped data
    - `politifact_web_scraping.py` scrapes PolitiFact data
    - `twitter_request.py` sends a request to the Users endpoint of the Twitter API
    - `utils.py` contains utility functions for batching Twitter requests
- `research` contains code for initial experiments
- `results` contains plots and statistics from the descriptive analytics
- `modeling.ipynb` runs the logistic regression and random forest models
- `negation_heuristic.ipynb` demonstrates the negation heuristic for the subtopic-level data collected