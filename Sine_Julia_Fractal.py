# -*- coding: utf-8 -*-
"""
Created on Sat May 23 21:46:51 2026

Created on Sat May 23 21:33:59 2026
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
# Create a Julia SET of Snn(z) Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/23

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_sine_julia():
    print("Initializing the transcendental c * sin(z) Julia set...")
    
    # 1. Framing and Resolution
    N = 2400  # High resolution for the delicate snowflake edges
    
    # The sine function creates repeating structures. 
    # A window of [-3.5, 3.5] perfectly frames the primary central snowflake.
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    
    max_iter = 1500
    escape_radius = 50.0  # Sine functions grow exponentially; 50 is plenty for escape

    # 2. Setup the complex plane (z_0)
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    # The exact parameter from your uploaded image
    c = -0.2 + 1.0j

    print(f"Iterating the series z = c * sin(z) with c = {c} ...")
    
    # 3. Escape-Time Iteration
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # The complex sine formula
            Z_new = c * np.sin(Z[alive])
            
        # Catch any infinite overflows caused by the exponential growth
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        # Check which points have escaped the radius
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Continuous smooth shading (Linear interpolation for transcendental functions)
        z_esc = Z[escaped]
        output[escaped] = i + 1 - np.log(np.abs(z_esc)) / np.log(escape_radius)
        
        alive &= (~escaped)
        
    # Points that never escape (the trapped core)
    output[alive] = max_iter

    print("Applying the Cream, Gold, Purple, and Crimson colormap...")
    
    # 4. Custom Colormap matching your reference image perfectly
    custom_colors = [
        # --- Outer Background (Fast Escapes) ---
        (0.00, '#FCFBF5'),  # Cream/White background
        (0.05, '#E8D5A5'),  # Pale tan/gold lace
        
        # --- The Main Snowflake Body ---
        (0.12, '#D4A35B'),  # Rich gold/mustard
        (0.20, '#A67C00'),  # Deep dark gold
        
        # --- The Blue/Purple Transition Rings ---
        (0.30, '#5E4A99'),  # Muted purple
        (0.40, '#3B5998'),  # Deep blue/violet
        
        # --- The Inner Spiral Valleys ---
        (0.55, '#B22222'),  # Deep firebrick red
        (0.70, '#FF3333'),  # Bright vibrant crimson
        
        # --- The Bottleneck Glow (Nearly Trapped Regions) ---
        (0.85, '#FF8C00'),  # Dark orange core edge
        (0.95, '#FFD700'),  # Bright yellow glow
        (1.00, '#FFFFFF')   # Pure white (The exact center trapped cores)
    ]
    sine_cmap = mcolors.LinearSegmentedColormap.from_list("sine_gold_purple", custom_colors)

    # 5. Render the final image
    plt.figure(figsize=(10, 10), facecolor='#FCFBF5')
    
    # We use a Gamma compression (PowerNorm) to push the purple and red colors 
    # tightly into the center, allowing the gold to spread across the wide outer arms.
    plt.imshow(output, cmap=sine_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.PowerNorm(gamma=0.6, vmin=0, vmax=max_iter * 0.5))
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Sine_Julia_Fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The image is saved to your folder as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_sine_julia()