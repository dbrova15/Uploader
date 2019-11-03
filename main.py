import os
import time
import queue
from multiprocessing import Pool as ThreadPool, Process


class Uploader(object):
    def __init__(self, file_list, n_treads, q):
        self.file_list = file_list
        self.n_treads = n_treads
        self.done = False
        self.error = 0
        self.total = 0
        q.put(self)

    def _upload_file(self, file):
        try:
            print(file)
            time.sleep(2)

        except Exception as e:
            print(e)
            self.error += 1
        finally:
            # print("finally", self.total)
            self.total = self.total + 1

        if self.total >= len(self.file_list):
            self.done = True

    def _upload_pool(self):
        pool = ThreadPool(processes=self.n_treads)
        pool.map(self._upload_file, self.file_list)

    def start(self):
        proc = Process(target=self._upload_pool)
        proc.start()
        print(1)

    def is_active(self):
        return self.done
        # if self.done:
        #     return False
        # else:
        #     return True


if __name__ == '__main__':
    q = queue.Queue()

    files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]

    uploader = Uploader(files_list, 2, q)
    uploader.start()

    while uploader.is_active():
        progress = q.get()
        print(uploader.is_active())
        print(progress.done, progress.error, progress.total)
