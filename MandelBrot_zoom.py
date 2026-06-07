# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 19:19:57 2026

@author: mcamp
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def generate_mandelbrot_zoom():
    print("Initializing Mandelbrot zoom sequence...")
    
    # --- Zoom Configuration ---
    num_frames = 150
    zoom_factor = 0.85  # 1.0 = no zoom. Lower = faster zoom per frame.
    
    # An incredibly detailed focal point in the Mandelbrot set (Seahorse Valley)
    center_x = -0.743665111
    center_y = 0.1318280027

    # Base boundaries for the Mandelbrot Set (Frame 0)
    base_width = 2.5   
    base_height = 2.5  

    # --- Fractal Parameters ---
    N = 500             
    max_iter = 500      
    escape_radius = 50.0 
    
    # Setup output folder
    output_dir = "mandelbrot_zoom_frames_500"
    os.makedirs(output_dir, exist_ok=True)

    # --- Build the Colormap Once ---
    colors = [
        (0.0,  '#FFFFFF'), (0.05, '#FFD700'), (0.20, '#FF4D4D'), 
        (0.40, '#B30000'), (0.48, '#660000'), (0.50, '#000000'), 
        (0.52, '#000000'), (0.55, '#003366'), (0.65, '#007FFF'), 
        (0.75, '#00C9FF'), (0.85, '#FFFF00'), (0.95, '#CCAA00'), 
        (1.00, '#e5f0f0') 
    ]
    mandel_cmap = mcolors.LinearSegmentedColormap.from_list("Mandelbrot_colors", colors)

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

        # Generate the complex plane for this frame.
        # CRITICAL FIX: For Mandelbrot, the grid becomes 'C'
        x = np.linspace(x_min, x_max, N, dtype=np.float64)
        y = np.linspace(y_min, y_max, N, dtype=np.float64)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        
        # Z is initialized to 0 for the Mandelbrot set
        Z = np.zeros_like(C)
        
        output = np.zeros(C.shape, dtype=np.float64)
        alive = np.ones_like(C, dtype=bool)

        # The math iteration
        for i in range(max_iter):
            with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
                # The Mandelbrot recurrence relation
                Z[alive] = Z[alive]**2 + C[alive]
                
            escaped = (np.abs(Z) > escape_radius) & alive
            z_escaped = Z[escaped]
            
            # Smooth shading
            output[escaped] = i + 1 - np.log2(np.log(np.abs(z_escaped)) / np.log(escape_radius))
            alive &= (~escaped)
            
        output[alive] = max_iter

        # Plotting the frame
        fig = plt.figure(figsize=(8, 8), facecolor='white')
        
        plt.imshow(output, cmap=mandel_cmap, extent=[x_min, x_max, y_min, y_max], 
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
    generate_mandelbrot_zoom()