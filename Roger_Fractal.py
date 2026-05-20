# -*- coding: utf-8 -*-
"""
Created on Wed May 20 05:26:39 2026

@author: mcamp
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_roger_fractal():
    print("Initializing fractal parameters...")
    
    # 1. Image resolution and framing
    N = 3000 # High resolution for crisp swirls
    
    # These boundaries frame the vertical shape well
    x_min, x_max = -2.0, 2.0
    y_min, y_max = -2.5, 2.5
    
    max_iter = 80
    escape_radius = 50.0

    # 2. Create the complex plane grid
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    
    # For this type of fractal, z starts as the coordinate plane itself
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating iterations... (this will take a few seconds)")
    
    # 3. Iterate the specific formula
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # Extract the current absolute value of Z
            abs_z = np.abs(Z[alive])
            
            # The formula: z^2 + (|z| + i) / (1 + |z|)
            dynamic_c = (abs_z + 1j) / (1.0 + abs_z)
            Z_new = Z[alive]**2 + dynamic_c
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        # Check which points have escaped
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Apply smooth continuous shading to get the fluid swirl look
        z_escaped = Z[escaped]
        output[escaped] = i + 1 - np.log2(np.log(np.abs(z_escaped)))
        
        alive &= (~escaped)
        
    # Cap the points that never escape
    output[alive] = max_iter

    print("Applying the fiery blue-red colormap...")
    
    # 4. Custom Color Palette matching your reference image
    colors = [
        (0.00, '#ffffff'),  # Pure White background
        (0.10, '#d1d9e6'),  # Soft light blue-grey halo
        (0.25, '#2b4162'),  # Dark slate blue
        (0.40, '#111d4a'),  # Very deep midnight blue
        (0.60, '#c70039'),  # Deep crimson red
        (0.75, '#ff5733'),  # Fiery orange
        (0.90, '#ffc300'),  # Bright yellow swirls
        (1.00, '#ffffff')   # White glowing cores
    ]
    roger_cmap = mcolors.LinearSegmentedColormap.from_list("roger_colors", colors)

    # 5. Render the final image
    plt.figure(figsize=(8, 10), facecolor='white')
    
    plt.imshow(output, cmap=roger_cmap, extent=[x_min, x_max, y_min, y_max], origin='lower')
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'roger_fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05, dpi=300)
    print(f"Done! The image is saved to your folder as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_roger_fractal()