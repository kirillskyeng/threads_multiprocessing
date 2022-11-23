import sys
import asyncio
import concurrent.futures
import time
from math import floor
from multiprocessing import cpu_count

import aiofiles
import aiohttp
from bs4 import BeautifulSoup


async def get_and_scrape_pages(num_pages: int, output_file: str):
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
    async with \
    aiohttp.ClientSession() as client, \
    aiofiles.open(output_file, "a+", encoding="utf-8") as f:

        for _ in range(num_pages):
            async with client.get("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status > 399:
                    # можно получить 429 Too Many Requests
                    # тогда вызываем исключение HTTPError
                    response.raise_for_status()

                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text

                await f.write(title + "\t")

        await f.write("\n")


def start_scraping(num_pages: int, output_file: str, i: int):
    # фикс  Exception ignored in 'RuntimeError: Event loop is closed'
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    """ Стартуем процесс акинхронного запроса и скрапинга Вики страниц """
    print(f"Процесс {i} стартует...")
    asyncio.run(get_and_scrape_pages(num_pages, output_file))
    print(f"Процесс {i} завершен.")


def main():
    NUM_PAGES = 30  # количество страниц для скрапинга
    NUM_CORES = cpu_count()  # количество логических ядер
    OUTPUT_FILE = "./wiki_titles.tsv"  # файл в который пишем

    PAGES_PER_CORE = floor(NUM_PAGES / NUM_CORES)
    PAGES_FOR_FINAL_CORE = PAGES_PER_CORE + NUM_PAGES % PAGES_PER_CORE  # для последнего ядра

    futures = []

    with concurrent.futures.ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(1, NUM_CORES):
            new_future = executor.submit(
                start_scraping,  # таск (функция)
                num_pages=PAGES_PER_CORE,  # аргументы
                output_file=OUTPUT_FILE,
                i=i
            )
            futures.append(new_future)

        futures.append(
            executor.submit(
                start_scraping,
                PAGES_FOR_FINAL_CORE, OUTPUT_FILE, NUM_CORES
            )
        )

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    print("Старт: Подождите, это может занять время (около 10 секунд)....")
    start = time.time()
    main()
    print(f"Завершено за: {round(time.time() - start, 2)} секунд.")
