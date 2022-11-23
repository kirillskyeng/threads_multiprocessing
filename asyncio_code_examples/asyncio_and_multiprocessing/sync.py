import time
import urllib.request

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
                    # тогда вызываем исключение
                    raise Exception(f"Получен статус {response.status} вместо 200.")

                page = response.read()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text
                f.write(title + "\t")

        f.write("\n")


def main():
    NUM_PAGES = 30  # количество страниц для скрапинга
    OUTPUT_FILE = "./wiki_titles.tsv"  # файл в который пишем

    get_and_scrape_pages(NUM_PAGES, OUTPUT_FILE)


if __name__ == "__main__":
    print("Старт: Подождите, это может занять время (около 60 секунд)....")
    start = time.time()
    main()
    print(f"Завершено за: {round(time.time() - start, 2)} секунд.")
