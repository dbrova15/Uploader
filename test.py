import sys
from time import sleep
from queue import Queue
from threading import Thread, enumerate

# Создаем FIFO очередь
q = Queue()


# Функция генерирующая данные для очереди
def source(n):
    for i in range(1, 1 + n): yield i


# Функция заполняющая очередь заданиями
def put(n):
    for item in source(n): q.put(item)


def worker():
    while True:
        # Если заданий нет - закончим цикл
        if q.empty(): sys.exit()
        # Получаем задание из очереди
        item = q.get()
        print(u'Очередь: %s выполняется' % item)
        # Сообщаем о выполненном задании
        q.task_done()
        print(u'Очередь: %s завершилась' % item)


# Создаем и запускаем потоки, которые будут обслуживать очередь
for x in range(1, 4):
    print(u'Поток', str(x), u'стартовал')

    put(x)
    Thread(target=worker).start()

    sleep(2)

print('Over')