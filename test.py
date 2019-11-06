import os
import unittest
from multiprocessing.dummy import Manager

from main import Uploader


class Test(unittest.TestCase):
    def first_test(self):
        q = Manager().Queue()

        files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]

        uploader = Uploader(files_list, 2, q)
        uploader.start()

        while uploader.is_active:
            progress = q.get()
            # print(progress)

    # def second_test(self):
    #     q = Manager().Queue()
    #
    #     files_list = ""
    #
    #     uploader = Uploader(files_list, 2, q)
    #     uploader.start()


if __name__ == '__main__':
    unittest.main()
