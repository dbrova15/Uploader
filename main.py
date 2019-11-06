import os
import time
from collections import Counter
from multiprocessing.dummy import Pool as ThreadPool, Process, Manager


class Uploader(object):

    def __init__(self, file_list, n_treads, q):
        assert isinstance(file_list, (list, tuple))
        assert isinstance(n_treads, int)
        assert n_treads >= 0
        assert type(q) is Manager().Queue

        self.is_active = True
        self.file_list = file_list
        self.n_treads = n_treads
        self.q = q

    def _upload_file(self, file):
        try:
            """ code uploader to FTP"""
            time.sleep(2)

        except Exception as e:
            self.q.put("Error! File {} is not loaded.\n{}".format(file, e))
            return False
        finally:
            self.q.put("Success! File {} is uploaded to the server.".format(file))
            return True
        # return "done"

    def _upload_pool(self):
        pool = ThreadPool(processes=self.n_treads)
        res = pool.map(self._upload_file, self.file_list)
        n_res = len(res)
        res_dict = Counter(res)
        succes = res_dict[True]
        self.q.put("Uploaded {}/{}".format(succes, n_res))
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
