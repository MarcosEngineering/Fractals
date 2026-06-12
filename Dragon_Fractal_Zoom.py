# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:52:24 2026

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
# Create a Dragon_Julia Fractal Zoom
# 
#----------------------------------------
# Author : Marco Campolo 2026/06/04

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def generate_dragon_zoom():
    print("Initializing Dragon Julia zoom sequence...")
    
    # --- Zoom Configuration ---
    num_frames = 200
    zoom_factor = 0.85  # 1.0 = no zoom. Lower = faster zoom per frame.
     
    center_x = 0.257555
    center_y = 0.03454998986

    # Base boundaries (Frame 0)
    base_width = 3.0   # From -1.5 to +1.5
    base_height = 2.4  # From -1.2 to +1.2

    # --- Fractal Parameters ---
    c = -0.54 + 0.54j
    N = 5000             
    max_iter = 500      
    escape_radius = 50.0 
    
    # Setup output folder
    output_dir = "dragon_zoom_frames"
    os.makedirs(output_dir, exist_ok=True)

    # --- Build the Colormap Once ---
    colors = [
        (0.0,  '#FFFFFF'), (0.05, '#FFD700'), (0.20, '#FF4D4D'), 
        (0.40, '#B30000'), (0.48, '#660000'), (0.50, '#000000'), 
        (0.52, '#000000'), (0.55, '#003366'), (0.65, '#007FFF'), 
        (0.75, '#00C9FF'), (0.85, '#FFFF00'), (0.95, '#CCAA00'), 
        (1.00, '#e5f0f0') 
    ]
    dragon_cmap = mcolors.LinearSegmentedColormap.from_list("Dragon_colors", colors)

    # --- Main Rendering Loop ---
    for frame in range(num_frames):
        print(f"Rendering frame {frame+1}/{num_frames}...")
        
        # Calculate new boundaries based on zoom factor
        current_width = base_width * (zoom_factor ** frame)
        current_height = base_height * (zoom_factor ** frame)
        
        x_min = center_x - (current_width / 2)
        x_max = center_x + (current_width / 2)
        y_min = center_y - (current_height / 2)
        y_max = center_y + (current_height / 2)

        # Generate the complex plane for this frame
        x = np.linspace(x_min, x_max, N, dtype=np.float64)
        y = np.linspace(y_min, y_max, N, dtype=np.float64)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        output = np.zeros(Z.shape, dtype=np.float64)
        alive = np.ones_like(Z, dtype=bool)

        # The math iteration
        for i in range(max_iter):
            with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
                Z[alive] = Z[alive]**2 + c
                
            escaped = (np.abs(Z) > escape_radius) & alive
            z_escaped = Z[escaped]
            
            # Smooth shading
            output[escaped] = i + 1 - np.log2(np.log(np.abs(z_escaped)) / np.log(escape_radius))
            alive &= (~escaped)
            
        output[alive] = max_iter

        # Plotting the frame
        fig = plt.figure(figsize=(8, 8), facecolor='white')
        
        plt.imshow(output, cmap=dragon_cmap, extent=[x_min, x_max, y_min, y_max], 
                   origin='lower', norm=mcolors.PowerNorm(gamma=0.4, vmin=0, vmax=max_iter))
        
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save the frame
        filename = os.path.join(output_dir, f"frame_{frame:03d}.png")
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.0, dpi=150)
        
        # CRITICAL: Close the figure so RAM doesn't fill up!
        plt.close(fig)

    print(f"\nSuccess! All {num_frames} frames are saved in the '{output_dir}' folder.")

if __name__ == "__main__":
    generate_dragon_zoom()