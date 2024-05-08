from threading import Thread
from multiprocessing import Process


CONCURRENCY_CLASS = (None, Thread, Process)
WORKERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
LOAD = (1, 100, 1000, 100000, 1000000)
CASES = [
    (c_class, workers, load)
    for load in LOAD
    for c_class in CONCURRENCY_CLASS
    for workers in WORKERS
]

if __name__ == "__main__":
    print("case,load,ctype,workers")

    for i, c in enumerate(CASES):
        ctype = "None" if c[0] is None else c[0].__name__
        workers = c[1]
        load = c[2]

        print(f"{i},{load},{ctype},{workers}")
