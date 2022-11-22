"""Написать программу, которая создает миниатюры изображений в папке images и сохраняет их в папке thumbs"""
import time
import os
from PIL import Image, ImageFilter
import multiprocessing

filenames = [
    'images/1.jpg',
    'images/2.jpg',
    'images/3.jpg',
    'images/4.jpg',
    'images/5.jpg',
]


def create_thumbnail(filename, size=(50, 50), thumb_dir='thumbs'):
    img = Image.open(filename)
    img = img.filter(ImageFilter.GaussianBlur())
    img.thumbnail(size)
    img.save(f'{thumb_dir}/{os.path.basename(filename)}')
    print(f'Файл {filename} обработан...')


if __name__ == '__main__':
    start = time.perf_counter()

    # однопроцессорное исполнение
    # for filename in filenames:
    #     create_thumbnail(filename)


    # создаем процесс
    processes = [multiprocessing.Process(target=create_thumbnail, args=[filename])
                for filename in filenames]

    # запускаем процесс
    for process in processes:
        process.start()

    # дожидаемся выполнение
    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f'Выполнение заняло {finish - start:} секунд.')
