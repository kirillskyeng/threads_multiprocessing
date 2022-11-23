import asyncio


async def count_to_three():
    print("Старт")
    await asyncio.sleep(4)
    print("Спал 4 секунды")
    await asyncio.sleep(1)
    print("Спал 1 секунду")
    await asyncio.sleep(0)
    print("Спал 0 секунд")
    print("Финиш")

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(count_to_three()))
loop.close()