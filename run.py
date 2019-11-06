import os
from multiprocessing import Manager

from main import Uploader

q = Manager().Queue()

files_list = [os.path.join(os.getcwd(), "test_data", i) for i in os.listdir("./test_data")]
uploader = Uploader(files_list, 2, q)
uploader.start()

while uploader.is_active:
    progress = q.get()
    print(progress)