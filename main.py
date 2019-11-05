from __future__ import annotations
import os
import time
from multiprocessing import Pool as ThreadPool, Process, Manager, Value

from typing import Optional

#
# class Progress:
#     def __init__(self):
#         self.done = False
#         self.total = 0
#         self.error = 0


class SingletonMeta(type):
    _instance: Optional[Progress] = None

    def __call__(self) -> Progress:
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance


class Progress(metaclass=SingletonMeta):
    def __init__(self):
        self.done = False
        self.total = 0
        self.error = 0
        # self.n_files = n_files


class Uploader(object):
    def __init__(self, file_list, n_treads, q):

        # self.n_file = Value("i", len(file_list))
        # self.error = Value("i", 0)
        # self.total = Value("i", 0)
        # self.done = Value("b", False)
        self.file_list = file_list
        # self.file_list = [{"file": i, "error": self.error, "total": self.total, "done": self.done, "n_file": self.n_file} for i in file_list]
        self.n_treads = n_treads
        self.done = False
        self.error = 0
        self.total = 0
        # progress = Progress()
        # q.put(progress) #{"done": self.done, "error": self.error, "total": self.total, "n_files": len(file_list)})
        self.q = q

    def _upload_file(self, file):
        # progress = self.q.get()
        # file = data["file"]
        # error = data["error"]
        # total = data["data"]
        # done = data["done"]
        # n_file = data["n_file"]

        try:
            # print(file)
            """ code uploader to FTP"""
            time.sleep(2)

        except Exception as e:
            print(e)
            # progress["error"] = + 1
            # progress.error =+ 1
            self.error += 1 #todo не меняеться значение
            self.q.put("Error! File {} is not loaded.".format(file))
        finally:
            # print("finally", self.total)
            # progress["total"] = + 1
            # progress.total = + 1
            self.total = self.total + 1  # todo не меняеться значение
            self.q.put("Success! File {} is uploaded to the server.".format(file))

        # if progress.n_files > 0:
        #     progress.n_files =- 1
        # else:
        #     progress.done = True
        #     self.done = True

        # if progress["n_files"] > 0:
        #     progress["n_files"] =-1
        # else:
        #     progress["done"] = True
        #     self.done = True

        # self.q.put(progress)
        # if self.total >= len(self.file_list):
        #     self.done = True  #todo не меняеться значение
        # progress =
        # self.q.put((self.error, self.total))

    def _upload_pool(self):
        pool = ThreadPool(processes=self.n_treads)
        pool.map(self._upload_file, self.file_list)

    def start(self):
        proc = Process(target=self._upload_pool)
        proc.start()
        # print(1)

    def is_active(self):
        # return self.done
        # print("is_active", self.done)
        if self.done:
            return False
        else:
            return True


if __name__ == '__main__':
    q = Manager().Queue()

    files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]
    # q.put({"done": False, "error": 0, "total": 0, "n_files": len(files_list)})
    uploader = Uploader(files_list, 2, q)
    uploader.start()

    while uploader.is_active():
        progress = q.get()
        # print(uploader.is_active())
        print(progress)
        # print(progress.done, progress.error, progress.total)
