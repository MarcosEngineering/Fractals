# -*- coding: utf-8 -*-
"""
Created on Sat May 23 21:33:59 2026

@author: mcamp
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
import warnings

def generate_packed_mandelbrot():
    print("1. Calculating the Mandelbrot Set Boundary...")
    
    # Setup high-resolution grid
    width, height = 1500, 1500
    x_min, x_max = -2.1, 0.7
    y_min, y_max = -1.4, 1.4
    
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    
    # Iterate to find the shape
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for _ in range(100):
            Z = Z**2 + C
            
    # Create a boolean mask (True if inside the Mandelbrot set)
    mask = np.abs(Z) <= 2
    
    print("2. Computing Distance Transform (Finding the edges)...")
    # This calculates how far every inside pixel is from the outside void
    distance_map = ndimage.distance_transform_edt(mask)
    pixel_size = (x_max - x_min) / width
    
    print("3. Executing Space-Filling Circle Packing Algorithm...")
    attempts = 40000          # Number of random seeds to try dropping
    min_radius = 0.003        # Smallest allowed ring
    padding_factor = 0.92     # Leaves a tiny gap between rings so they don't touch
    
    # Store circles as [x, y, radius]
    circles = np.empty((0, 3))
    
    for i in range(attempts):
        # Pick a random pixel
        px = np.random.randint(0, width)
        py = np.random.randint(0, height)
        
        # If it's outside the fractal, ignore it
        if not mask[py, px]:
            continue
            
        c_x = x[px]
        c_y = y[py]
        
        # Max radius before it hits the fractal boundary
        max_r_fractal = distance_map[py, px] * pixel_size
        
        # Max radius before it hits another existing circle
        if len(circles) > 0:
            dist_to_circles = np.hypot(circles[:, 0] - c_x, circles[:, 1] - c_y)
            space_available = dist_to_circles - circles[:, 2]
            max_r_circles = np.min(space_available)
        else:
            max_r_circles = np.inf
            
        # The circle can only grow as large as the tightest constraint
        r = min(max_r_fractal, max_r_circles)
        
        # If there is enough room, plant the circle!
        if r > min_radius:
            new_circle = np.array([[c_x, c_y, r * padding_factor]])
            circles = np.vstack([circles, new_circle])
            
        # Print progress
        if i % 10000 == 0 and i > 0:
            print(f"   ... tried {i} seeds, packed {len(circles)} circles so far.")

    print(f"Finished packing! Total circles perfectly fit: {len(circles)}")
    print("4. Rendering 3D Torus Geometries...")

    # Set up the canvas
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_aspect('equal')
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.axis('off')

    # Draw each circle as a multi-layered 3D ring
    for cx, cy, r in circles:
        # Giant rings become Ruby Red
        if r > 0.15:
            c_dark  = '#4D0000'  # Deep maroon background shadow
            c_mid   = '#B30000'  # Rich crimson mid-tone
            c_high  = '#FF6666'  # Bright pink/red highlight
            c_inner = '#260000'  # Near-black red inner shadow
        # Smaller packing rings become Sapphire Blue
        else:
            c_dark  = '#001A4D'  # Deep navy background shadow
            c_mid   = '#005CE6'  # Vibrant royal blue mid-tone
            c_high  = '#66B2FF'  # Glowing cyan/ice highlight
            c_inner = '#000A1A'  # Near-black blue inner shadow

        # Layering patches to create a 3D bevel/torus effect
        ax.add_patch(plt.Circle((cx, cy), r,        facecolor=c_dark, edgecolor='none'))
        ax.add_patch(plt.Circle((cx, cy), r * 0.88, facecolor=c_mid,  edgecolor='none'))
        ax.add_patch(plt.Circle((cx, cy), r * 0.75, facecolor=c_high, edgecolor='none'))
        ax.add_patch(plt.Circle((cx, cy), r * 0.55, facecolor=c_inner,edgecolor='none'))
        ax.add_patch(plt.Circle((cx, cy), r * 0.40, facecolor='white',edgecolor='none'))

    plt.tight_layout()
    filename = 'Packed_Mandelbrot.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! Image saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_packed_mandelbrot()