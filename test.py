import os
import unittest
from multiprocessing.dummy import Manager

from main import Uploader

q = Manager().Queue()
files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]


class Test(unittest.TestCase):
    def test_1(self):
        self.assertIsInstance(Uploader(files_list, 2, q), Uploader)

    def test_2(self):
        self.assertIsInstance(Uploader("", 2, q), Uploader)

    def test_3(self):
        self.assertIsInstance(Uploader(files_list, "2", q), Uploader)

    def test_4(self):
        self.assertIsInstance(Uploader(files_list, 2, "q"), Uploader)


if __name__ == '__main__':
    unittest.main()
