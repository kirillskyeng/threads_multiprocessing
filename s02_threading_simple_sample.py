"""Модуль threading для мультипоточных проограмм"""

from time import sleep, perf_counter
from threading import Thread


def task():
    print('Начинаем выполнение задачи...')
    sleep(1)
    print('Выполнено')


start_time = perf_counter()

# создаем два новых потока
t1 = Thread(target=task)
t2 = Thread(target=task)

# запускаем потоки
t1.start()
t2.start()

# главный поток будет ждать завершения t1, t2 потоков
# t1.join()
# t2.join()

end_time = perf_counter()

print(f'Выполнение заняло {end_time - start_time} секунд.')
