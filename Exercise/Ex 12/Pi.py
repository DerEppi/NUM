# from ex 9.1

import numpy as np
import threading
from multiprocessing import Pool, cpu_count


xmin, xmax = -1, 1
ymin, ymax = xmin, xmax

R = (xmax - xmin) / 2
xc = 0.5 * (xmin + xmax)
yc = 0.5 * (ymin + ymax)


def pi(P):
    x = np.random.uniform(xmin, xmax, P)
    y = np.random.uniform(ymin, ymax, P)

    inside = (x-xc)**2 + (y-yc)**2 < R
    n = np.sum(inside)

    return 4*n / P


# threaded
def pi_worker(P, results, idx):
    x = np.random.uniform(xmin, xmax, P)
    y = np.random.uniform(ymin, ymax, P)

    inside = (x - xc)**2 + (y - yc)**2 < R**2
    results[idx] = np.sum(inside)

def pi_threaded(P, nthreads=4):
    threads = []
    results = [0] * nthreads

    chunk = P // nthreads

    for i in range(nthreads):
        t = threading.Thread(target=pi_worker, args=(chunk, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return 4 * sum(results) / P




def inside(P):
    x = np.random.uniform(xmin, xmax, P)
    y = np.random.uniform(ymin, ymax, P)

    inside = (x - xc)**2 + (y - yc)**2 <= R**2
    return np.sum(inside), P


def pi_parallel(P):
    nproc = cpu_count()  

    chunksize = [P // nproc]

    with Pool(processes=nproc) as pool:
        results = pool.map(inside, chunksize)

    inside_total = sum(r[0] for r in results)
    P_total = sum(r[1] for r in results)

    return 4 * inside_total / P_total


import time

if __name__ == "__main__":
    P = int(1e8)

    print("\nProcessing...\n")

    # --- serial ---
    start = time.perf_counter()
    pi_val = pi(P)
    end = time.perf_counter()
    print(f"\nSerial pi: {pi_val:.6f}, time: {end - start:.4f} s")

    # --- threading ---
    start = time.perf_counter()
    pi_val = pi_threaded(P, nthreads=4)
    end = time.perf_counter()
    print(f"\nThreaded pi: {pi_val:.6f}, time: {end - start:.4f} s")

    # --- multiprocessing ---
    start = time.perf_counter()
    pi_val = pi_parallel(P)
    end = time.perf_counter()
    print(f"\nMultiprocessing pi: {pi_val:.6f}, time: {end - start:.4f} s")
