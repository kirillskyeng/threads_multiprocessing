import asyncio


async def say1():
    await asyncio.sleep(1)
    print("Hello 1!")


async def say2():
    await asyncio.sleep(1)
    print("Hello 2!")


print("start")
loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(say1(), say2()))
print("exit")

loop.close()
