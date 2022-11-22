from multiprocessing import Process
import os
import time


def square_numbers():
    for i in range(50):
        _ = i * i
        time.sleep(0.1)


if __name__ == '__main__':
    start_time = time.perf_counter()

    processes = []
    num_processes = 10  # os.cpu_count()
    # type cmd: WMIC CPU Get DeviceID,NumberOfCores,NumberOfLogicalProcessors

    # create processes
    for _ in range(num_processes):
        p = Process(target=square_numbers)
        processes.append(p)

    # start processes
    for p in processes:
        p.start()

    # join
    for p in processes:
        p.join()

    end_time = time.perf_counter()
    print('end of main')
    print('duration:', end_time - start_time)
