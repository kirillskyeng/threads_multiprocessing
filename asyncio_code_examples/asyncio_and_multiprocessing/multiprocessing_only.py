import concurrent.futures
import time
import urllib.request
from math import floor
from multiprocessing import cpu_count

from bs4 import BeautifulSoup


def get_and_scrape_pages(num_pages: int, output_file: str):
    """
    Отправляет запрос в Википедию для возврата случайных страниц.
    Скарирует каждую полученную страницу по ее заголовку с помощью BeautifulSoup,
    затем добавляет его в указанный файл через табуляцию.

    #### Аргументы
    ---
    num_pages: int -
        количество страниц для запроса и скрапинга страницы в поиске заголовка

    output_file: str -
        файл для добавления заголовков
    """
    with open(output_file, "a+", encoding="utf-8") as f:
        for _ in range(num_pages):
            with urllib.request.urlopen("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status > 399:
                    # можно получить 429 Too Many Requests
                    # тогда вызываем исключение HTTPError
                    raise Exception(f"Received a {response.status} instead of 200.")

                page = response.read()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text
                f.write(title + "\t")

        f.write("\n")


def main():
    NUM_PAGES = 30  # количество страниц для скрапинга
    NUM_CORES = cpu_count()  # количество логических ядер
    OUTPUT_FILE = "./wiki_titles.tsv"  # файл в который пишем

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE  # для последнего ядра

    futures = []
    with concurrent.futures.ThreadPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES - 1):
            new_future = executor.submit(
                get_and_scrape_pages,  # таск (функция)
                num_pages=PAGES_PER_CORE,  # аргументы
                output_file=OUTPUT_FILE,
            )
            futures.append(new_future)

        futures.append(
            executor.submit(
                get_and_scrape_pages,
                PAGES_FOR_FINAL_CORE, OUTPUT_FILE
            )
        )

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    print("Старт: Подождите, это может занять время (около 20 секунд)....")
    start = time.time()
    main()
    print(f"Завершено за: {round(time.time() - start, 2)} секунд.")
