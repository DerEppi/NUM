import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
import time

# Image parameters
width, height = 4000, 2800
max_iter = 300
xmin, xmax = -2.0, 1.0
ymin, ymax = -1.5, 1.5

# Create a grid of complex numbers
real = np.linspace(xmin, xmax, width)
imag = np.linspace(ymin, ymax, height)
c = real[np.newaxis, :] + 1j * imag[:, np.newaxis]

# Initialize the iteration counts
escape_iter = np.zeros(c.shape, dtype=int)
z = np.zeros(c.shape, dtype=complex)

def mandelbrot_chunk(args):
    y_start, y_end, real, imag = args
    height_chunk = y_end - y_start
    rows = np.zeros((height_chunk, real.size), dtype=int)
    z = np.zeros((height_chunk, real.size), dtype=complex)
    c = real[np.newaxis, :] + 1j * imag[y_start:y_end, np.newaxis]

    for i in range(max_iter):
        mask = np.abs(z) <= 2
        if not mask.any():
            break
        z[mask] = z[mask] ** 2 + c[mask]
        rows[mask & (np.abs(z) > 2)] = i
    return rows

if __name__ == "__main__":
    # Split the work into chunks
    n_processes = cpu_count()
    chunk_size = height // n_processes
    chunks = [(i * chunk_size, (i + 1) * chunk_size, real, imag) for i in range(n_processes)]

    start = time.time()

    with Pool(processes=n_processes) as pool:
        results = pool.map(mandelbrot_chunk, chunks)

    escape_iter = np.vstack(results)

    print(f"process time: {(time.time()-start):.3f} s")

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.imshow(escape_iter, extent=(xmin, xmax, ymin, ymax), cmap='hot', origin='lower')
    plt.colorbar(label='Escape iteration')
    plt.title('Mandelbrot Set (Parallelized)')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.show()