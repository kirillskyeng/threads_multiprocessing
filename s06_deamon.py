"""
Потоки-демоны выполняют задачи в фоновом режиме.

Примеры задач:
- Запись информации в файл в фоновом режиме.
- Скраппинг содержимого веб-сайта в фоновом режиме.
- Автоматическое сохранение данных в базе данных в фоновом режиме.
"""

from threading import Thread
import time


def show_timer():
    count = 0
    while True:
        count += 1
        time.sleep(1)
        print(f'Прошло {count} секунд...')


t = Thread(target=show_timer, daemon=True)  # сравнить с True
t.start()

answer = input('Вы хотите выйти?\n')
