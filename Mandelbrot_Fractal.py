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
# Create a graph with MandelBrot Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/16


from PIL import Image

# drawing area (complex plane boundaries)
xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5

# max iterations allowed (increased for finer detail at high resolutions)
maxIt = 512 

# image size (increased to 2048x2048 for a bigger image)
imgx = 2048
imgy = 2048

image = Image.new("RGB", (imgx, imgy))
# Optimization: load() allocates a memory map for lightning-fast pixel writing
pixels = image.load()

print(f"Generating {imgx}x{imgy} Mandelbrot set. This might take a moment...")

for y in range(imgy):
    zy = y * (yb - ya) / (imgy - 1)  + ya
    for x in range(imgx):
        zx = x * (xb - xa) / (imgx - 1)  + xa
        z = zx + zy * 1j
        c = z
        
        for i in range(maxIt):
            if abs(z) > 2.0: 
                break 
            z = z * z + c
            
        # Coloring the pixels
        if i == maxIt - 1:
            # The point is inside the Mandelbrot set; color it black
            pixels[x, y] = (0, 0, 0)
        else:
            # The point escaped; color it based on how fast it escaped
            pixels[x, y] = (i % 4 * 64, i % 8 * 32, i % 16 * 16)

image.save("Mandelbrot_Fractal.pdf", "PDF")
print("Done! Saved as Mandelbrot_Fractal.pdf")
