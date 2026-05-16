# -*- coding: utf-8 -*-
"""
Created on Sat May 16 14:21:15 2026


Copyright (c) 2026, Campolo Marco
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.


"""

#----------------------------------------
# Create a graph IABS Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/16

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def iabs(z):
    """Absolute value applied only to the imaginary component."""
    return z.real + 1j * np.abs(z.imag)

def generate_detailed_tree_fractal():
    print("Setting up high-detail parameters...")
    
    # 1. High resolution and deep iteration limit to reveal the trees
    N = 1500
    x_min, x_max = -3.0, 2.0
    y_min, y_max = -2.5, 2.5
    
    # INCREASED max_iter: This forces the computer to look deeper into the white blob
    max_iter = 300 
    escape_radius = 100.0

    # 2. The precise complex constant
    c = 0.555 + 0.15j 

    # 3. Create the complex grid
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating deep iterations... (this may take 10-20 seconds)")
    
    # 4. Iterate the formula
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            inner_term = (Z[alive] + c)**2 - 1.0
            inner_term[inner_term == 0] = 1e-10 + 1e-10j
            
            Z_new = np.sinh(np.log(iabs(inner_term)))
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Color the escaped points (the background and the two holes)
        # We use a smooth calculation to make the gradients look nice
        z_escaped = Z[escaped]
        output[escaped] = i + 1 - np.log(np.log(np.abs(z_escaped))) / np.log(2.0)
        
        alive &= (~escaped)
        
    # 5. INTERIOR COLORING (The magic trick!)
    # Instead of leaving the trapped points solid white, we color them based 
    # on their final mathematical magnitude to reveal the complex tree structures.
    final_magnitude = np.abs(Z[alive]) * 50
    # We wrap the values so they cycle through our colors smoothly
    output[alive] = final_magnitude % max_iter

    print("Rendering with the vibrant target palette...")
    
    # 6. Exact Color Palette matching your target
    # White background -> Blue -> Purple -> Red -> Orange -> Yellow trees
    # colors = [
    #     (0.00, '#ffffff'),  # Pure White (Fast escaping background/holes)
    #     (0.10, '#6688FF'),  # Light Blue
    #     (0.35, '#5500AA'),  # Deep Purple
    #     (0.60, '#FF0055'),  # Pink/Red
    #     (0.80, '#FF8800'),  # Orange
    #     (1.00, '#FFFF00')   # Bright Yellow (Deepest tree branches)
    # ]
    
    colors = [
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
    
    custom_cmap = mcolors.LinearSegmentedColormap.from_list("tree_colors", colors)

    # 7. Render the final image
    plt.figure(figsize=(10, 10), facecolor='white')
    
    plt.imshow(output, cmap=custom_cmap, extent=[x_min, x_max, y_min, y_max], origin='lower')
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'iabs_fractal_2.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05, dpi=300)
    print(f"Done! The high-detail image is saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_detailed_tree_fractal()