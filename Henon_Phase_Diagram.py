# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:18:51 2026

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
# Create a Henon Phase Diagram
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/24

import numpy as np
import matplotlib.pyplot as plt

def generate_henon_phase_diagram(a=1.6, num_orbits=150, iters_per_orbit=2000):
    print(f"Generating Hénon phase diagram for a = {a}...")
    
    # 1. Setup figure with a dark background to match the reference image
    fig, ax = plt.subplots(figsize=(4, 4), facecolor='black')
    ax.set_facecolor('black')
    
    # Precompute trigonometry for performance
    cos_a = np.cos(a)
    sin_a = np.sin(a)
    
    # 2. Define initial conditions
    # By taking a line of points along the x-axis, we intersect the stable center, 
    # the chaotic sea, and the satellite islands.
    x0_values = np.linspace(0.0, 1.0, num_orbits)
    
    # 3. Use the 'turbo' or 'jet' colormap to replicate the exact color gradient
    cmap = plt.get_cmap('turbo')
    
    for i, x0 in enumerate(x0_values):
        # Arrays to hold the orbit's coordinates
        x = np.zeros(iters_per_orbit)
        y = np.zeros(iters_per_orbit)
        x[0], y[0] = x0, 0.0
        
        # Color mapping based on distance from the origin
        color = cmap(i / num_orbits)
        
        for n in range(iters_per_orbit - 1):
            # The Hénon map formulas
            x_new = x[n] * cos_a - (y[n] - x[n]**2) * sin_a
            y_new = x[n] * sin_a + (y[n] - x[n]**2) * cos_a
            
            # If the orbit escapes to infinity, stop tracking it
            if x_new**2 + y_new**2 > 100:
                x = x[:n]
                y = y[:n]
                break
                
            x[n+1] = x_new
            y[n+1] = y_new
            
        # 4. Scatter plot for this specific orbit
        # We use a very small point size (s) and transparency (alpha) to create the fine dust effect
        if len(x) > 0:
            ax.scatter(x, y, s=0.05, color=color, alpha=0.6, edgecolors='none')
        
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout()
    
    # Save and show
    filename = f'Henon_Phase_a_{a}.pdf'
    plt.savefig(filename, facecolor='black', dpi=300, bbox_inches='tight')
    print(f"Success! Saved to {filename}")
    plt.show()

if __name__ == "__main__":
    generate_henon_phase_diagram(a=1.6)