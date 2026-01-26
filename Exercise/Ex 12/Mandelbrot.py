import numpy as np
import matplotlib.pyplot as plt
import time

# Image parameters
width, height = 2000, 1400
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

start = time.time()

# Mandelbrot iteration
for i in range(max_iter):
    mask = np.abs(z) <= 2
    z[mask] = z[mask] ** 2 + c[mask]
    escape_iter[mask & (np.abs(z) > 2)] = i

print(f"process time: {(time.time()-start):.3f} s")

plt.figure(figsize=(12, 8))
plt.imshow(escape_iter, extent=(xmin, xmax, ymin, ymax), cmap='magma', origin='lower')
plt.colorbar(label='Escape iteration')
plt.title('Mandelbrot Set')
plt.xlabel('Re(c)')
plt.ylabel('Im(c)')
plt.show()



