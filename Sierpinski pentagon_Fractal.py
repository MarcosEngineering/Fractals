# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 23:20:21 2026

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

import numpy as np 
import matplotlib.pyplot as plt
from numba import njit

@njit  # Compiles the function to C-speed for fast point generation
def generate_midpoint_chaos(num_points=10000000):
    # Standard chaos game scaling factor (moving halfway)
    s = 0.5 
    
    # Generate vertices for a regular pentagon
    angles = np.linspace(0, 2 * np.pi, 6)[:-1]
    vertices = np.empty((5, 2))
    for i in range(5):
        vertices[i, 0] = np.cos(angles[i])
        vertices[i, 1] = np.sin(angles[i])
    
    points = np.zeros((num_points, 2))
    current_point = np.array([0.0, 0.0]) 
    
    for i in range(1, num_points):
        # 1. Choose one seed at random
        seed1 = np.random.randint(0, 5)
        
        # 2. Choose the second seed as two after the first randomly chosen seed
        seed2 = (seed1 + 2) % 5
        
        # 3. The target is the midpoint of these two specific seeds
        target_midpoint = (vertices[seed1] + vertices[seed2]) / 2.0
        
        # Move halfway from the current point towards the target midpoint
        current_point = current_point * s + target_midpoint * (1 - s)
        points[i] = current_point
        
    return points

# 1. Generate the fractal points (ignoring the first 100 to let it settle)
print("Generating fractal points...")
points = generate_midpoint_chaos(num_points=10000000)
x, y = points[100:, 0], points[100:, 1]

# 2. Plot using a 2D histogram to achieve the density/heatmap look
print("Rendering image...")
plt.figure(figsize=(8, 8), facecolor='white')

# The 'inferno' colormap closely matches the dark blue to yellow gradient on the right side of the image
# You can change 'inferno' to 'gray' to match the grayscale version on the left side of the image
plt.hist2d(x, y, bins=1200, cmap='inferno', cmin=1)

plt.axis('equal')
plt.axis('off') 
plt.tight_layout()

filename = 'Sierpinski_pentagon_fractal.jpg'
plt.savefig(filename, bbox_inches='tight', pad_inches=0.05, dpi=300)
print(f"Done! The image is saved to your folder as '{filename}'.")
plt.show()