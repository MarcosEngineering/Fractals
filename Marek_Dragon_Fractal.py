# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:36:23 2026

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
# Create Marek Dragon Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/26

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

def generate_marek_dragon():
    print("Initializing Marek Dragon parameters...")
    
    # 1. Calculate the specific irrational parameter 'r' from the text
    r = 1.0 - (math.sqrt(2) - math.sqrt(3) + math.sqrt(5)) / 2.0
    
    # 2. Calculate the complex constant z_c = e^(2 * pi * i * r)
    zc = np.exp(2j * np.pi * r)
    
    # 3. Resolution and framing parameters
    N = 1200
    x_min, x_max = -1.5, 0.5
    y_min, y_max = -1.5, 1.0
    
    max_iter = 1000
    escape_radius = 50.0  # High escape radius for smooth gradient shading

    # 4. Setup the complex plane (z_0)
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print(f"Iterating z = z_c * z + z^2 (where r ≈ {r:.4f})...")
    
    # 5. Escape-Time Iteration with Smooth Shading
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # The exact math formula: z_{n+1} = z_c * z_n + z_n^2
            Z_new = zc * Z[alive] + Z[alive]**2
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # Smooth shading algorithm for continuous gray gradients
        z_esc = Z[escaped]
        output[escaped] = i + 1 - np.log2(np.log(np.abs(z_esc)))
        
        alive &= (~escaped)
        
    output[alive] = max_iter

    print("Applying the silver and charcoal colormap...")
    
    # 6. Custom Colormap
    custom_colors = [
       
        (0.00, '#000000'), # Pure black (Fastest escape / Deepest background)
        (0.02, '#000C33'), # Midnight blue (Smooths the harsh jump from black)
        (0.05, '#0028FF'), # Deep Blue 
        (0.12, '#006BD6'), # Azure/Royal Blue (Bridges deep blue to the teal)
        (0.20, '#00B2B2'), # Cyan-Teal
        (0.30, '#1AD9D9'), # Vibrant mid-Cyan
        (0.40, '#4CFFFF'), # Bright neon Cyan
        (0.44, '#73FFFF'), # Lighter ice-Cyan
        (0.48, '#99FFFF'), # Pale Cyan (Approaching the boundary)
        (0.49, '#CCFFFF'), # Icy near-white (Creates a "bloom" effect)
        (0.50, '#FFFFFF'), # The sharp Julia set boundary (Pure White)
        
       # --- Stable Region (Refined Negative Plasma) ---
        (0.52, '#FFFFFF'), # Inner Boundary of Ring (Pure White)
        (0.53, '#FFE6CC'), # Very pale peach (Smooths the bright white glare)
        (0.55, '#FFCC99'), # Peach/Light Orange
        (0.60, '#FFA64D'), # Soft Mango/Amber (Bridges peach to orange)
        (0.65, '#FF8000'), # Vibrant Orange
        (0.70, '#FF5900'), # Fiery Vermilion
        (0.75, '#FF3600'), # Red-Orange (The peak of the warm ring)
        
        # --- The Red-to-Blue Transition Zone ---
        (0.78, '#CC0066'), # Deep Magenta (Pulls the red toward blue)
        (0.82, '#6600CC'), # Vibrant Violet/Purple (Smooths the entry into pure blue)
        
        # --- The Cold Core ---
        (0.85, '#0000FF'), # Pure Blue (Vibrant center of the inner ring)
        (0.90, '#1A33FF'), # Royal Blue 
        (0.95, '#3355FF'), # Soft Blue
        (0.98, '#1A1A4D'), # Deep Navy Blue (Eases the blue down into the black void)
        (1.00, '#1A0F0F')  # Near Black (The trapped cores)
    ]
    marek_cmap = mcolors.LinearSegmentedColormap.from_list("marek_color", custom_colors)

    # 7. Render the final image
    plt.figure(figsize=(10, 10), facecolor='#C8C8C8')
    
    # PowerNorm compresses the grays to highlight the dark swirling boundaries
    plt.imshow(output, cmap=marek_cmap, extent=[x_min, x_max, y_min, y_max], 
               origin='lower', norm=mcolors.PowerNorm(gamma=0.6, vmin=0, vmax=max_iter * 0.75))
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Marek_Dragon.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The image is saved to your folder as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_marek_dragon()