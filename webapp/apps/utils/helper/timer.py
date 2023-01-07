import time


def time_function(func, *args):

    start = time.time()
    func(*args)
    end = time.time()
    print(f"Elapsed time: {end - start}")
    print("----------------------------")
