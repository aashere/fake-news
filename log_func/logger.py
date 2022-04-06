class Logger:
    log_success = False

    query_request_failed = []
    tweet_request_failed = []
    user_request_failed = []
    reply_request_failed = []

    def __init__(self, log_success=False):
        self.log_success = log_success

    def log_query_request_failure(self, id):
        self.query_request_failed.append(id)

    def dump(self):
        if self.query_request_failed:
            with open('log/request_log/query_request_failed.txt', 'w+') as f:
                f.write('\n'.join(self.query_request_failed))
        if self.tweet_request_failed:
            with open('log/request_log/tweet_request_failed.txt', 'w+') as f:
                f.write('\n'.join(self.tweet_request_failed))
        if self.user_request_failed:
            with open('log/request_log/user_request_failed.txt', 'w+') as f:
                f.write('\n'.join(self.user_request_failed))
        if self.reply_request_failed:
            with open('log/request_log/reply_request_failed.txt', 'w+') as f:
                f.write('\n'.join(self.reply_request_failed))

        if self.log_success:
            pass