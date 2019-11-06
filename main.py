import os
import time
from multiprocessing.dummy import Pool as ThreadPool, Process, Manager


class Uploader(object):

    def __init__(self, file_list, n_treads, q):
        assert file_list is not list
        assert n_treads is not int
        assert n_treads <= 0

        self.is_active = True
        self.file_list = file_list
        self.n_treads = n_treads
        self.q = q

    def _upload_file(self, file):
        try:
            """ code uploader to FTP"""
            time.sleep(2)

        except Exception as e:
            print(e)
            self.q.put("Error! File {} is not loaded.".format(file))
        finally:
            self.q.put("Success! File {} is uploaded to the server.".format(file))
        return "done"

    def _upload_pool(self):
        pool = ThreadPool(processes=self.n_treads)
        res = pool.map(self._upload_file, self.file_list)

        self.is_active = False

    def start(self):
        proc = Process(target=self._upload_pool)
        proc.start()


if __name__ == '__main__':
    q = Manager().Queue()

    files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]
    uploader = Uploader(files_list, 2, q)
    uploader.start()

    while uploader.is_active:
        progress = q.get()
        print(progress)
