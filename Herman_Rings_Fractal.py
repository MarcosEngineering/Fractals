# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:09:19 2026

@author: mcamp
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_herman_ring_fatou_components():
    print("Initializing high-accuracy fractal parameters...")
    
    # 1. Mathematical constants
    phi = (np.sqrt(5) - 1) / 2.0  # Golden ratio conjugate for ideal irrational rotation
    C = np.exp(2j * np.pi * phi)
    
    # 2. Optimized framing and resolution
    # A square frame centered around the unit circle gives the best view.
    width, height = 2400, 1600 
    x_min, x_max = -5.0, 9.0
    y_min, y_max = -4.0, 4.0
    
    # Increased iterations for sharper internal boundaries
    max_iter = 350 
    # Large escape radius for clean outer gradient
    escape_radius = 50.0 

    # 3. Create the complex grid
    x = np.linspace(x_min, x_max, width, dtype=np.float64)
    y = np.linspace(y_min, y_max, height, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Arrays to track the state of each point
    alive = np.ones_like(Z, dtype=bool)
    escape_times = np.zeros(Z.shape, dtype=int)
    
    # Dual array to hold color values
    color_indices = np.zeros(Z.shape, dtype=np.float64)
    
    print("Calculating iterations (this will take a moment)...")
    # 4. Iterate the specific formula: z_{n+1} = (C * z_n^2 * (z_n - 4)) / (1 - 4z_n)
    for i in range(max_iter):
        z_alive = Z[alive]
        
        # Calculate the denominator first to handle the pole at z = 0.25
        denominator = 1.0 - 4.0 * z_alive
        
        with np.errstate(divide='ignore', invalid='ignore'):
            z_new = (C * (z_alive**2) * (z_alive - 4.0)) / denominator
            
        # Handle potential NaNs or Infs that occur from division by zero
        z_new[~np.isfinite(z_new)] = 1e10
        Z[alive] = z_new
        
        # Check escapes
        abs_z = np.abs(Z)
        escaped_this_round = (abs_z > escape_radius) & alive
        escape_times[escaped_this_round] = i
        
        # Smooth coloring for background (external)
        if np.any(escaped_this_round):
            # Scale escape times 0-1 for background colormap
            color_indices[escaped_this_round] = (1.0 - (i / max_iter)) # Reversed so max iter is near 0
            
        alive &= (~escaped_this_round)

    # 5. Handle Stable Points (The Internal Ring)
    # This is the crucial part that distinguishes the ring and hole
    print("Processing stable internal components...")
    final_z_abs = np.abs(Z[alive])
    
    # The ring forms on an irrational path around the unit circle.
    # Points near z=0 converge to the fixed point (the hole).
    # We map the final absolute value (radius) of stable points to color values.
    # We use a custom, terrain-like map to create texture.
    # Points with radius close to 0 and points very far (for stable points) are mapped to dark/background.
    
    # We normalize these final radii to map them into a distinct colormap segment.
    # We use a non-linear scaling to match the texture in the reference.
    normalized_stable = 0.5 + 0.5 * (np.power(final_z_abs, 1.5) / np.power(2.0, 1.5))
    
    color_indices[alive] = normalized_stable

    # 6. Visual Setup - Advanced Custom Colormaps
    print("Rendering detailed Fatou components...")
    
    # Custom colormap segments:
    # 0.0 - 0.5: Exterior Escaping (Red/Orange gradient)
    # 0.5 - 1.0: Interior Stable (Vibrant Blue/Yellow terrain gradient)
    
    custom_colors = [
        (0.0,  '#FFFFFF'), # Pure white (fast escape)
        (0.05, '#FFD700'), # Gold/Yellow
        (0.20, '#FF4D4D'), # Bright glowing red
        (0.40, '#B30000'), # Crimson
        (0.48, '#660000'), # Deep maroon near stable boundary
        (0.50, '#000000'), # The sharp Julia set boundary (Black)
        
        # --- Stable Region ---
        (0.52, '#000000'), # Inner Boundary of Ring/Outer Hole (Black)
        (0.55, '#003366'), # Dark Blue (converging close to hole)
        (0.65, '#007FFF'), # Azure Blue (converging)
        (0.75, '#00C9FF'), # Cyan (beginning of main ring)
        (0.85, '#FFFF00'), # Pure Yellow (vibrant center of ring)
        (0.95, '#CCAA00'), # Darker Yellow
        (1.0,  '#FFFFFF')  # Bright white highlight
    ]
    custom_cmap = mcolors.LinearSegmentedColormap.from_list("HermanRingHybrid", custom_colors)

    # 7. Plotting
    plt.figure(figsize=(10, 10), facecolor='black')
    
    # The normalized color_indices can use a linear map
    norm = mcolors.Normalize(vmin=0, vmax=1)
    
    # interpolation='bilinear' softens the pixels into the organic shapes
    plt.imshow(color_indices, cmap=custom_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=norm, interpolation='bilinear')
    
    plt.axis('off')
    plt.tight_layout()
    
    # Save as high-resolution image to reveal detail
    print("Saving Herman_ring_Fractal.pdf...")
    plt.savefig('Herman_ring_Fractal.pdf', bbox_inches='tight', pad_inches=0, dpi=400)
    print("Done!")
    plt.show()

if __name__ == "__main__":
    generate_herman_ring_fatou_components()