import sys
import asyncio
import time

import aiohttp
import aiofiles


async def write_genre(file_name):
    """
    Выбирает случайный музыкальный жанр из binaryjazz.us,
    выводит его на экран и помещает в отдельный файл.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://binaryjazz.us/wp-json/genrenator/v1/genre/") as response:
            genre = await response.json()

    async with aiofiles.open(file_name, "w") as new_file:
        print(f"Пишем '{genre}' в '{file_name}'...")
        await new_file.write(genre)


async def main():
    tasks = []

    print("Старт...")
    start = time.time()

    for i in range(10):
        tasks.append(write_genre(f"./async/new_file{i}.txt"))

    await asyncio.gather(*tasks)

    end = time.time()
    print(f"Финиш. Время на асинхронное чтение/запись: {round(end - start, 2)} секунд")


if __name__ == "__main__":
    # фикс  Exception ignored in 'RuntimeError: Event loop is closed'
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
