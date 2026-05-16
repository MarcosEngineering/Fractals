"""
Created on Sun Dec 24 11:48:14 2023

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
# Create a graph with Lemon Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/16


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_smooth_peach_fractal():
    print("Setting up the parameters...")
    phi = -0.14
    N = 1500  # Resolution
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    max_iter = 60
    
    # We increase the escape radius significantly for smooth shading to work properly
    escape_radius = 100.0 

    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    Z[Z == 0] = 1e-10

    # Use float64 instead of int because smooth shading calculates decimal values
    output = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating iterations with smooth shading...")
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore'):
            Z_new = (Z[alive]**7 + phi) / Z[alive]
            
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        escaped = (np.abs(Z) > escape_radius) & alive
        
        # --- THIS IS THE MODIFICATION FOR THE SECOND IMAGE ---
        # Smooth coloring algorithm: nu = iter + 1 - log(log(|Z|)) / log(degree)
        # The degree of our equation is 7
        z_escaped = Z[escaped]
        smooth_val = i + 1 - np.log(np.log(np.abs(z_escaped))) / np.log(7.0)
        output[escaped] = smooth_val
        
        alive &= (~escaped)

    # For points that never escape
    output[alive] = max_iter

    print("Rendering the smooth image...")
       
    # Custom colormap segments:
    # 0.0 - 0.5: Exterior Escaping (Red/Orange gradient)
    # 0.5 - 1.0: Interior Stable (Vibrant Blue/Yellow terrain gradient)
    
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
    
    peach_cmap = mcolors.LinearSegmentedColormap.from_list("peach", colors)

    plt.figure(figsize=(10, 10), facecolor='white')
    
    # We no longer need PowerNorm because the smooth calculation handles the gradients
    plt.imshow(output, cmap=peach_cmap, extent=[x_min, x_max, y_min, y_max], origin='lower')
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Lemon_fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.05, dpi=300)
    print(f"Done! Image saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_smooth_peach_fractal()