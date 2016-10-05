from queue import Queue
from threading import Thread
from concurrent_demo import URLFetcher


class ThreadingUrlFetcher(URLFetcher):
    def setup_concurrency(self):
        # setup concurrency
        self.q = Queue(self.concurrency + 50)

        for i in range(self.concurrency):
            t = Thread(target=self.thread_worker)
            t.daemon = True
            t.start()

    def thread_worker(self):
        while True:
            item_id = self.q.get()
            item_data = self.fetch_item(item_id)
            if item_data is not None:
                self.process_item(item_data)
            self.q.task_done()

    def load_stories(self, item_ids):
        for item_id in item_ids:
            self.q.put(item_id)
        self.q.join()


ThreadingUrlFetcher().run()
