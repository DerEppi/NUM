import time
import random
import multiprocessing as mp

def rigged_dice():
    x = random.randint(1, 4)
    if x == 4:
        return 6
    else:
        return random.randint(1, 5)

def worker(n):
    count_6 = 0
    invalid = False
    for _ in range(n):
        x = rigged_dice()
        if x == 6:
            count_6 += 1
        elif x < 1 or x > 6:
            invalid = True
    return count_6, invalid


if __name__ == "__main__":
    
    # Sequential

    N = 10**9
    print(f"\nTotal calls: {N:.0e}")
    print(f"\nSimple version:\nprocessing...\n")
    start = time.time()

    count_6 = 0
    invalid = False

    for _ in range(N):
        x = rigged_dice()
        if x == 6:
            count_6 += 1
        elif x < 1 or x > 6:
            invalid = True

    elapsed = time.time() - start

    upper = N/4 + N/1000
    lower = N/4 - N/1000
    check = lower <= count_6 <= upper

    print(f"Number of sixes: {count_6}")
    print(f"Sixes in expected range ({lower:.0f}, {upper:.0f}): {"Yes" if check else "No"}")
    print(f"Any invalid values: {"Yes" if invalid else "No"}")
    print(f"Elapsed time: {elapsed:.1f} s")


    # Parallelized

    print("\n-------------------------------\n\nParallelized version:\nprocessing...\n")
    n_proc = mp.cpu_count()
    chunk = N // n_proc

    start = time.time()

    with mp.Pool(processes=n_proc) as pool:
        results = pool.map(worker, [chunk] * n_proc)

    total_6 = sum(r[0] for r in results)
    any_invalid = any(r[1] for r in results)

    elapsed = time.time() - start

    check = lower <= total_6 <= upper

    print(f"Processes: {n_proc}")
    print(f"Number of sixes: {total_6}")
    print(f"Sixes in expected range ({lower:.0f}, {upper:.0f}): {"Yes" if check else "No"}")
    print(f"Any invalid values: {"Yes" if any_invalid else "No"}")
    print(f"Elapsed time: {elapsed:.1f} s")

# for N=1e8: 
# Sequential: 96.8 s
# Parallel: 19.7 s
