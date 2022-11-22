from threading import Thread
import os
import time


def square_numbers():
    for i in range(100):
        _ = i * i
        time.sleep(0.1)


if __name__ == '__main__':
    start_time = time.perf_counter()

    threads = []
    num_threads = 10

    # create threads
    for _ in range(num_threads):
        t = Thread(target=square_numbers)
        threads.append(t)

    # start processes
    for t in threads:
        t.start()

    # join
    for t in threads:
        t.join()

    end_time = time.perf_counter()
    print('end of main')
    print('duration:', end_time - start_time)
