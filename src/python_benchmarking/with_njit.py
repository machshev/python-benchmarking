import sys
import numpy as np
from numba import njit

from .cases import CASES


@njit
def run(load, workers, c_class):
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


if __name__ == "__main__":
    case_id = int(sys.argv[-1])

    c_class, workers, load = CASES[case_id]

    run(load=load, workers=workers, c_class=c_class)
