# -*- coding: utf-8 -*-
"""
Created on Fri May 22 21:54:38 2026

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
# Create a Cubic Julia Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/22


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_deep_cubic_julia():
    print("Initializing deep iteration parameters...")
    
    # 1. High resolution for delicate lace details
    N = 2400 
    x_min, x_max = -1.6, 1.6
    y_min, y_max = -1.6, 1.6
    
    # CRITICAL FIX 1: Massive iteration increase to clear the bottleneck
    max_iter = 1000 
    
    # Higher escape radius for flawless smooth gradients
    escape_radius = 50.0  

    # 2. Setup the complex plane
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Pushing through the parabolic bottleneck... (This will take a few seconds)")
    
    # 3. Escape-Time Iteration
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # The exact perturbed cubic formula
            Z_new = Z[alive]**3 - (-Z[alive])**2.00001 + 1.0008875
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Smooth shading math adjusted for a cubic polynomial
        z_esc = Z[escaped]
        output[escaped] = i + 1 - np.log(np.log(np.abs(z_esc))) / np.log(3.0)
        
        alive &= (~escaped)
        
    output[alive] = max_iter

    print("Applying the high-contrast rust and crimson colormap...")
    
    # 4. Custom Colormap matching the target image exactly
    custom_colors = [
        # --- Outer Background (Fast Escapes) ---
        (0.00, '#FFFFFF'),  # Pure White background
        (0.03, '#FFFFFF'),  # Hold white to keep the outer space crisp
        (0.06, '#FCFBF5'),  # Barely-there ivory (softens the initial fade-in)
        (0.10, '#FDF9EE'),  # Pale cream
        
        # --- Outer Halos & Lace (Mid-speed Escapes) ---
        (0.15, '#F2E8C9'),  # Soft wheat/sand
        (0.20, '#E8D5A5'),  # Pale tan/gold
        (0.30, '#D4A35B'),  # Warm amber/ochre (bridges gold to rust smoothly)
        
        # --- The Heavy Structure (Slow Escapes) ---
        (0.40, '#C26A2D'),  # Rust/Copper (The main structural rings)
        (0.52, '#9E3C14'),  # Burnt umber/dark rust (Adds deep 3D shadows to the rings)
        (0.65, '#8A0F0F'),  # Deep crimson valleys
        
        # --- The Bottleneck Glow (Nearly Trapped Regions) ---
        (0.75, '#B80000'),  # Strong classic red (Eases crimson into bright red)
        (0.85, '#E60000'),  # Bright glowing red
        (0.93, '#FF6666'),  # Soft coral/pinkish bloom 
        (0.98, '#FFCCCC'),  # Very light blush halo
        (1.00, '#FFFFFF')   # Pure white (The exact center of the bottleneck cores)
    ]
    cubic_cmap = mcolors.LinearSegmentedColormap.from_list("cubic_rust", custom_colors)

    plt.figure(figsize=(10, 10), facecolor='white')
    
    # CRITICAL FIX 2: vmin/vmax compression
    # By clamping the color stretch to 350 (even though max_iter is 1000),
    # it packs the crimson and rust bands tightly together to create distinct rings.
    plt.imshow(output, cmap=cubic_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.PowerNorm(gamma=0.55, vmin=0, vmax=350))
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Cubic_Julia_Fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The true deep fractal is saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_deep_cubic_julia()