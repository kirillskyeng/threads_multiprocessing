import sys
import time
import asyncio                 # Даст нам async/await
import aiohttp                 # Для асинхронного выполнения HTTP запросов
import aiofiles                # Дла асинхронного выполнения операций с файлами
import concurrent.futures      # Позволяет создать новый процесс
from multiprocessing import cpu_count # Вернет количество ядер процессора
from bs4 import BeautifulSoup  # Для скрапинга страниц
from math import floor         # Поможет разделить запросы между ядрами CPU


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

# 1. aiohttp.ClientSession() - для асинхронного открытия сеанса.
# позволяет делать HTTP-запросы и оставаться подключенными к источнику, не блокируя выполнение нашего кода

# 2. async with aiofiles - для асинхронного открытия файла для записи

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


def main():
    NUM_PAGES = 30  # количество страниц для скрапинга
    OUTPUT_FILE = "./wiki_titles.tsv" # файл для добавления заголовков

    get_and_scrape_pages(NUM_PAGES, OUTPUT_FILE)


if __name__ == "__main__":
    # фикс  Exception ignored in 'RuntimeError: Event loop is closed'
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    print("Старт: Подождите, это может занять время (порядка 20 секунд)....")
    start = time.time()
    # asyncio.run(main())
    print(f"Завершено за: {round(time.time() - start, 2)} секунд.")
