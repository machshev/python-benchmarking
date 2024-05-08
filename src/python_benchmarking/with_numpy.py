import sys
import math
from threading import Thread
from multiprocessing import Process

import numpy as np
from numba import njit


def simple_division(load, workers, c_class):
    """Divide values by 5, without any storage"""
    items = load * 10000

    def worker(start, stop):
        for i in range(start, stop):
            i / 5

    if c_class is None:
        worker(1, items)
        return

    pool = []
    work_split = np.linspace(0, items, num=workers + 1, endpoint=True, dtype=int)
    for w in range(workers):
        start = work_split[w]
        stop = work_split[w + 1]

        t = c_class(target=worker, args=(start, stop))
        t.start()

        pool.append(t)

    for t in pool:
        t.join()


def simple_division_numpy(load, workers, c_class):
    """Divide values by 5, without any storage"""
    items = load * 10000

    def worker(start, stop):
        np.arange(start, stop, dtype=int) / 5

    if c_class is None:
        worker(1, items)
        return

    pool = []
    work_split = np.linspace(0, items, num=workers + 1, endpoint=True, dtype=int)
    for w in range(workers):
        start = work_split[w]
        stop = work_split[w + 1]

        t = c_class(target=worker, args=(start, stop))
        t.start()

        pool.append(t)

    for t in pool:
        t.join()


simple_division_njit = njit(simple_division_numpy)


def peace_of_pi(load, workers, c_class):
    """Use Leibniz infinite series to go through the motions of calculating pi"""
    items = load * 1000

    def worker(name, results, initial, count, sign=1, sign_diff=-1, spacing=2):
        total = 0

        val = initial

        for _ in range(count):
            # print(f"{name} {sign}/{val}")
            total += sign / val
            val += spacing
            sign *= sign_diff

        results.append(total)

    totals = []
    if c_class is None:
        worker("1", totals, 1, items)

    else:
        pool = []
        count = int(items / workers)
        excess = items % workers

        spacing = 2 * workers
        sign_diff = 1 if (1 + workers) % 2 else -1

        for w in range(workers):
            initial = 1 + w * 2
            w_count = count + 1 if w < excess else count

            sign = 1 if (1 + w) % 2 else -1

            t = c_class(
                target=worker,
                args=(w, totals, initial, w_count, sign, sign_diff, spacing),
            )
            t.start()

            pool.append(t)

        for t in pool:
            t.join()


ALGS = (
    simple_division,
    simple_division_numpy,
    simple_division_njit,
    # peace_of_pi,
)
CONCURRENCY_CLASS = (None, Thread, Process)
WORKERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
LOAD = (1, 10, 100, 1000)  # (10, 100, 1000, 10000)
CASES = [
    (algorithm, c_class, workers, load)
    for algorithm in ALGS
    for c_class in CONCURRENCY_CLASS
    for workers in WORKERS
    for load in LOAD
]

if __name__ == "__main__":
    if sys.argv[-1] == "help":
        for i, c in enumerate(CASES):
            algorithm_name = c[0].__name__
            ctype = "None" if c[1] is None else c[1].__name__
            workers = c[2]
            load = c[3]

            print(f"{i},{algorithm_name},{ctype},{workers},{load}")

        num_of_cases = len(CASES)
        print(f"number of cases: {num_of_cases}")
        exit()

    if sys.argv[-1] == "join":
        bench = []
        with open("bench.csv", "r") as f:
            for l in f.readlines():
                bench.append(l.strip().split(","))

        with open("bench.full.csv", "w") as f:
            f.write(",".join(bench[0] + ["alg", "type", "workers", "load"]) + "\n")

            for i, c in enumerate(CASES):
                algorithm_name = c[0].__name__
                ctype = "None" if c[1] is None else c[1].__name__
                workers = c[2]
                load = c[3]
                f.write(
                    ",".join(
                        str(v)
                        for v in bench[i + 1] + [algorithm_name, ctype, workers, load]
                    )
                    + "\n"
                )
        exit()

    if len(sys.argv) != 2:
        raise ValueError("Expected arg: [CASE]")

    run = int(sys.argv[-1])

    alg, c_class, workers, load = CASES[run]

    alg(load=load, workers=workers, c_class=c_class)
