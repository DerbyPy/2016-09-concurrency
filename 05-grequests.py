from concurrent_demo import URLFetcher
import grequests


class GRequestsURLFetcher(URLFetcher):
    concurrency = 50

    def setup_concurrency(self):
        pass

    def load_stories(self, item_ids):
        self.requests = []
        for item_id in item_ids:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
            self.requests.append(grequests.get(url, timeout=self.requests_timeout))

    def process_stories(self):
        for response in grequests.imap(self.requests, self.concurrency):
            item_data = response.json()
            self.process_item(item_data)


GRequestsURLFetcher().run()
