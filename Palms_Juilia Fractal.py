# -*- coding: utf-8 -*-
"""
Created on Wed May 20 20:17:24 2026

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
# Create Palms_Julia Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/21



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_Palms_julia():
    print("Initializing high-detail Julia set parameters...")
    
    # The exact mathematical constant
    c = 0.37 + 0.1j
    
    # 1. Ultra-high resolution to capture the microscopic threads
    N = 5000 
    x_min, x_max = -1.2, 1.2
    y_min, y_max = -1.2, 1.2
    
    # 2. CRITICAL FIX: Massive increase in iterations to resolve the deep spirals
    max_iter = 500 
    
    # 3. CRITICAL FIX: Larger escape radius for flawless smooth shading
    escape_radius = 50.0 

    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating deep iterations... (This will take a few seconds)")
    
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            Z[alive] = Z[alive]**2 + c
            
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Standardized smooth shading equation
        z_escaped = Z[escaped]
        output[escaped] = i + 1 - np.log2(np.log(np.abs(z_escaped)) / np.log(escape_radius))
        
        alive &= (~escaped)
        
    output[alive] = max_iter

    print("Applying the sharp, compressed colormap...")
    
    
    colors = [
        # --- Escaping Region (Background to Boundary) ---
        (0.0,  '#E6D5B8'), # Sable/Sand background (fast escape)
        (0.05, '#DFCDA0'), # Smooth transition sand
        (0.20, '#D9C27A'), # Smooth warm sand/yellow 
        (0.40, '#216327'), # Deep forest green (The outer crisp boundaries)
        (0.48, '#0A2E10'), # Very dark green near boundary
        (0.50, '#000000'), # The sharp Julia set boundary (Black)
        
        # --- Stable Region (Inside the Fractal) ---
        (0.52, '#000000'), # Inner Boundary of Ring/Outer Hole (Black)
        (0.55, '#0A2E10'), # Deep emerald green (converging close to hole)
        (0.65, '#008F39'), # Classic vivid green (converging)
        (0.75, '#32CD32'), # Lime green (beginning of main ring)
        (0.85, '#ADFF2F'), # Green-yellow (vibrant center of ring)
        (0.95, '#D4FFB2'), # Pale bright green
        (1.00, '#F0FFF0')  # Icy white-green (The trapped cores)
    ]
    Julia_cmap = mcolors.LinearSegmentedColormap.from_list("Julia_colors", colors)

    plt.figure(figsize=(10, 10), facecolor='white')
    
    # 4. CRITICAL FIX: PowerNorm(gamma=0.4) tightly compresses the colors 
    # to highlight the dark fractal lines instead of washing them out.
    plt.imshow(output, cmap=Julia_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.PowerNorm(gamma=0.4, vmin=0, vmax=max_iter))
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Palms_Julia_Fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The deep spiral image is saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_Palms_julia()