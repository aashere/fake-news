import re
from datetime import datetime, timedelta, timezone
from time import strptime

month_to_num = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
}

# Assumes article time looks like:
# March 23, 2022
def article_time_to_utc(article_time):
    m = re.match('([a-zA-Z]+) ([0-9]+), ([0-9]+)', article_time)
    assert m is not None

    month = month_to_num[m.group(1)]
    day = m.group(2)
    if int(day) < 10:
        day = '0' + str(int(day))
    year = m.group(3)

    utc_timestamp = year + '-' + month + '-' + day + 'T00:00:00Z'
    return utc_timestamp

# Get timestamp 5 days before today
def get_end_time_timestamp(days=5):
    time_now = datetime.now(timezone.utc)
    delta = timedelta(days=days)

    range_start = time_now - delta
    return str(range_start)[:10] + 'T00:00:00Z'

def is_timestamp_in_range(timestamp, end_time):
    timestamp = strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_time = strptime(end_time, "%Y-%m-%dT%H:%M:%SZ")

    return max(timestamp, end_time) == timestamp