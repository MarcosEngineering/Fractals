# -*- coding: utf-8 -*-
"""
Created on Thu May 21 19:34:52 2026
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



#---------------------------------------------
# Create Gasket Julia Fractal Graph
# 
#---------------------------------------------
# Author : Marco Campolo 2026/05/21
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def generate_rational_gasket():
    print("Initializing Rational Map parameters...")
    
    # 1. The exact constant specified at the bottom of your image
    c = -2.0 + 0.0j
    
    # 2. Resolution and framing
    N = 1200 
    
    # A wide coordinate window to capture the full oval shape
    x_min, x_max = -4.5, 4.5
    y_min, y_max = -4.5, 4.5
    
    # 60 iterations is enough to reveal the intricate web
    max_iter = 60

    # 3. Setup the complex plane
    x = np.linspace(x_min, x_max, N, dtype=np.float64)
    y = np.linspace(y_min, y_max, N, dtype=np.float64)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    output = np.zeros(Z.shape, dtype=int)
    alive = np.ones_like(Z, dtype=bool)

    print("Calculating convergence to the fixed attractor at z = 1 ...")
    
    # 4. Iterate the Rational Formula
    for i in range(max_iter):
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            
            # z^4 + z^2 + 1 / z^4 - z^2 + 1
            z2 = Z[alive]**2
            z4 = z2**2
            
            numerator = z4 + z2 + 1.0
            denominator = z4 - z2 + 1.0
            
            Z_new = (numerator / denominator) + c
            
        # Catch any points that hit the division-by-zero poles
        Z_new[~np.isfinite(Z_new)] = 1e10
        Z[alive] = Z_new
        
        # CRITICAL DIFFERENCE: 
        # Check if the point has converged to the attractor at z = 1
        converged = (np.abs(Z - 1.0) < 1e-2) & alive
        
        # We record the exact step it converged to recreate those distinct color bands
        output[converged] = i
        alive &= (~converged)
        
    # The fractal web itself consists of the points that NEVER converge
    output[alive] = max_iter

    # print("Applying the pale green and rust colormap...")
    
    # 5. Color Palette matching your reference image
    #  colors = [
    #    (0.00, '#eef2cd'),  # Pale yellow-green (Fast convergence / Background)
    #    (0.15, '#d9e09b'),  # Light lime/yellow
    #    (0.40, '#edaa45'),  # Orange
    #    (0.75, '#c75612'),  # Rust red/orange (Slow convergence)
    #    (1.00, '#661a02')   # Deep rust (The trapped fractal web itself)
    # ]
    
    print("Applying the deep red and blush colormap...")
    
    colors = [
        (0.00, '#FCE8E8'),  # Pale blush pink (Fast convergence / Background)
        (0.15, '#F08080'),  # Light coral red
        (0.40, '#DC143C'),  # Vivid crimson red
        (0.75, '#8B0000'),  # Deep dark red (Slow convergence)
        (1.00, '#2B0000')   # Very dark, almost black maroon (The trapped fractal web itself)
    ]
    gasket_cmap = mcolors.LinearSegmentedColormap.from_list("gasket", colors)

    # 6. Render the final image
    plt.figure(figsize=(10, 10), facecolor='white')
    
    plt.imshow(output, cmap=gasket_cmap, extent=[x_min, x_max, y_min, y_max], origin='lower')
    
    plt.axis('off')
    plt.tight_layout()
    
    filename = 'Gasket_fractal.pdf'
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=300)
    print(f"Success! The image has been saved as '{filename}'.")
    plt.show()

if __name__ == "__main__":
    generate_rational_gasket()