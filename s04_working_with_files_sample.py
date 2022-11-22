"""Есть список текстовых файлов. Заменить текст во всех файлах."""
from time import perf_counter
from threading import Thread


def replace(filename, substr, new_substr):
    print(f'Обрабатываем файл {filename}')
    # получаем содержимое файла
    with open(filename, 'r') as f:
        content = f.read()

    # заменяем substr на new_substr
    content = content.replace(substr, new_substr)

    # записываем данные в файл
    with open(filename, 'w') as f:
        f.write(content)


def single_thread(filenames):
    for filename in filenames:
        replace(filename, 'lorem', 'lorems')


def multi_thread(filenames):
    # создаем потоки
    threads = [Thread(target=replace, args=(filename, 'lorems', 'lorem')) for filename in filenames]

    # запускаем потоки
    for thread in threads:
        thread.start()

    # ждем завершения потоков
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    filenames = [
        'archive/test1.txt',
        'archive/test2.txt',
        'archive/test3.txt',
        'archive/test4.txt',
        'archive/test5.txt',
        'archive/test6.txt',
        'archive/test7.txt',
        'archive/test8.txt',
        'archive/test9.txt',
        'archive/test10.txt',
    ]

    # тестируем однопоточное исполнение
    start_time = perf_counter()
    single_thread(filenames)  # run
    end_time = perf_counter()
    print(f'Выполнение заняло {end_time - start_time} секунд.')

    # тестируем многопоточное исполнение
    start_time = perf_counter()
    multi_thread(filenames)  # run
    end_time = perf_counter()
    print(f'Выполнение заняло {end_time - start_time} секунд.')
