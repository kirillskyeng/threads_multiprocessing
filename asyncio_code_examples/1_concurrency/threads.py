import json
import threading
import time
from urllib.request import Request, urlopen


def write_genre(file_name):
    """
    Выбирает случайный музыкальный жанр из binaryjazz.us,
    выводит его на экран и помещает в отдельный файл.
    """

    req = Request("https://binaryjazz.us/wp-json/genrenator/v1/genre/", headers={"User-Agent": "Chrome/107.0.0.0"})
    genre = json.load(urlopen(req))

    with open(file_name, "w") as new_file:
        print(f"Пишем '{genre}' в '{file_name}'...")
        new_file.write(genre)


if __name__ == "__main__":

    threads = []

    print("Старт...")
    start = time.time()

    for i in range(10):
        thread = threading.Thread(
            target=write_genre,
            args=[f"./threading/new_file{i}.txt"]
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end = time.time()
    print(f"Финиш. Время на потоковое чтение/запись: {round(end - start, 2)} секунд")
