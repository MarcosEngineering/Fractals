# -*- coding: utf-8 -*-
"""
Created on Fri May 22 22:32:27 2026

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

def generate_true_cubic_julia():
    print("Initializing the deep Log-Scaled Cubic Julia...")
    
    # 1. Framing and Resolution
    N = 2400  
    x_min, x_max = -1.6, 1.6
    y_min, y_max = -1.6, 1.6
    
    # CRITICAL FIX 1: Massive iteration increase to close the white holes
    max_iter = 3000 
    escape_radius = 50.0  

    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating 3000 iterations... (This will take a moment to clear the bottleneck)")
    
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # The exact perturbed cubic formula
            Z_new = Z[alive]**3 - (-Z[alive])**2.00001 + 1.0008875
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Smooth shading (we add 10 to ensure all values are well above 1 for LogNorm)
        z_esc = Z[escaped]
        output[escaped] = i + 10 - np.log(np.log(np.abs(z_esc))) / np.log(3.0)
        
        alive &= (~escaped)
        
    output[alive] = max_iter + 10

    print("Applying Logarithmic Color Scaling...")
    
    # 2. Custom Colormap matching the target image
    # --- Refined Cream, Rust, & Crimson Palette ---
    custom_colors = [
        # 1. The Canvas (Fast escapes)
        (0.00, '#FFFFFF'),  # Pure White background
        (0.05, '#FEFCF5'),  # Extremely pale ivory (softens the harsh white edge)
        (0.15, '#FDF9EE'),  # Cream
        
        # 2. The Outer Lace (Mid-speed escapes)
        (0.25, '#F1E3BD'),  # Soft sandy gold transition
        (0.35, '#E8D5A5'),  # Rich Gold/Tan
        (0.45, '#D5A062'),  # Warm ochre/light rust
        
        # 3. The Deep Structure (Slow escapes)
        (0.55, '#C26A2D'),  # True Rust
        (0.65, '#A63D17'),  # Burnt orange/dark rust (Adds 3D depth to the rings)
        (0.75, '#8A0F0F'),  # Deep Crimson
        
        # 4. The Glowing Cores (Trapped/Nearly trapped)
        (0.85, '#B30000'),  # Intense dark red (Bridges crimson to the bright glow)
        (0.92, '#E60000'),  # Bright Glowing Red
        (0.97, '#FFCCCC'),  # Soft blush pink (Smooths the harsh jump to pure white)
        (1.00, '#FFFFFF')   # The deep central pinprick cores
    ]
    cubic_cmap = mcolors.LinearSegmentedColormap.from_list("cubic_rust", custom_colors)

    plt.figure(figsize=(10, 10), facecolor='white')
    
    # CRITICAL FIX 2: LogNorm perfectly distributes the massive iteration plateau,
    # pulling the rust, crimson, and red colors beautifully into the deep lobes.
    plt.imshow(output, cmap=cubic_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.LogNorm(vmin=8.0, vmax=max_iter + 10))
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Cubic_Fractal_2.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The true deep fractal is saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_true_cubic_julia()