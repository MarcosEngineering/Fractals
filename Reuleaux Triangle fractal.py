# -*- coding: utf-8 -*-
"""
Created on Fri May 15 10:24:25 2026


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
import matplotlib.colors as mcolors

# 1. Modifications for the Mathematical Parameters
PHI = -1.7 / 3.0

# 2. Increase the Resolution for More Detail
N = 10000

# 3. Adjust Iterations and Escape Threshold
MAX_ITER = 30
ESCAPE_RADIUS = 25.0

# 4. Modify the Color Map to Mimic Metal (Custom Grayscale-to-Red)
custom_red_colors = [
    (0.0, 'black'),
    (0.15, '#2A0000'), # Very dark blood red
    (0.40, '#660000'), # Deep maroon
    (0.70, '#B30000'), # Strong crimson
    (0.95, '#FF4D4D'), # Bright glowing red/coral
    (1.0, 'white')     # Pure highlight
]

# Define the colormap variable
red_cmap = mcolors.LinearSegmentedColormap.from_list("red_metal", custom_red_colors)

def compute_iteration(z, phi):
    """Computes one step of the modified Newton-like system."""
    with np.errstate(divide='ignore', invalid='ignore'):
        result = (z**3 + phi) / z
    result[~np.isfinite(result)] = 1e20
    return result

def generate_complex_fractal(width, height, max_iter, phi, escape_radius):
    """Generates the escape-time fractal map."""
    re_min, re_max = -1.8, 1.8
    im_min, im_max = -1.5, 1.5
    
    r1 = np.linspace(re_min, re_max, width, dtype=np.float32)
    r2 = np.linspace(im_min, im_max, height, dtype=np.float32)
    re, im = np.meshgrid(r1, r2)
    z = re + 1j * im
    
    alive = np.ones_like(z, dtype=bool)
    output = np.zeros(z.shape, dtype=int)
    
    for i in range(max_iter):
        z[alive] = compute_iteration(z[alive], phi)
        escaped_this_round = (np.abs(z) > escape_radius) & alive
        output[escaped_this_round] = i
        alive &= (~escaped_this_round)
        
    return output

# 5. Execute, Render, and Plot
print("Generating the fractal geometry...")
fractal_data = generate_complex_fractal(N, N, MAX_ITER, PHI, ESCAPE_RADIUS)
print("Geometry complete. Applying the custom metal texture rendering...")

plt.figure(figsize=(10, 10), facecolor='#111111') # Added a dark background to the figure itself
# Apply the corrected metallic color map
plt.imshow(fractal_data, cmap=red_cmap, extent=[-1.8, 1.8, -1.5, 1.5], origin='lower',
           norm=mcolors.PowerNorm(0.7, vmin=0, vmax=MAX_ITER))
plt.axis('off') # Hide axes for a clean geometric image
plt.tight_layout()

print("Saving and showing the base mathematical visualization...")
# Save the file (this will save in the same folder where you run the script)
plt.savefig('Releaux_Triangle_fractal.pdf', bbox_inches='tight', pad_inches=0, dpi=300)
plt.show()
print("Done.")