# -*- coding: utf-8 -*-
"""
Created on Fri May 22 21:03:42 2026

@author: mcamp
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_classic_julia():
    print("Initializing Paul Bourke's classic Julia set...")
    
    # The complex constant 'c'. 
    # Change these numbers to get a completely different fractal!
    c = -0.7639 - 0.1j 
    
    # Image resolution and framing
    N = 10000
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    
    max_iter = 100
    # For z^2 + c, math proves that if it passes a radius of 2.0, it will escape to infinity
    escape_radius = 2.0 

    # 1. Map each pixel to a rectangular region of the complex plane (as the text states)
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    
    # 2. The initial value z_0 for the series is each point in the image plane
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=int)
    alive = np.ones_like(Z, dtype=bool)

    print(f"Calculating iterations for z = z^2 + ({c.real} + {c.imag}i)...")
    
    # 3. Compute the series for each pixel
    for i in range(max_iter):
        # The classic iterated function: z_{n+1} = z_n^2 + c
        Z[alive] = Z[alive]**2 + c
        
        # Decision procedure to determine divergence
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Colouring the point by how fast it diverges to infinity
        output[escaped] = i
        alive &= (~escaped)
        
    # If the series hasn't diverged, it is assigned to be part of the set
    output[alive] = max_iter

    print("Rendering the image...")
    
    # Create a nice dark space and glowing blue/gold colormap
    colors = [
        (0.00, '#000000'),  # Black (escapes instantly)
        (0.10, '#101540'),  # Deep space blue
        (0.40, '#2d50a8'),  # Bright blue
        (0.80, '#f2d05e'),  # Gold
        (1.00, '#000000')   # Black (The interior of the set that never escapes)
    ]
    julia_cmap = mcolors.LinearSegmentedColormap.from_list("julia", colors)

    # Render
    plt.figure(figsize=(10, 10), facecolor='black')
    plt.imshow(output, cmap=julia_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.PowerNorm(gamma=0.7))
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'julia_set_2.png'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! Check your folder for '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_classic_julia()