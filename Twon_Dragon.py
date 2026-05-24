# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:32:53 2026

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
# Create a Twon Dragon Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/24

import sys
import math
import random
import time
import numpy as np
from PIL import Image

# --- Constants ---
NX = 2000
NY = 2000
N = 100000000  # 100 Million iterations
SCALE = NX / 5.0

def main():
    # 1. Argument Parsing (Updated for IDEs)
    if len(sys.argv) < 2:
        print("No argument provided. Defaulting to m = 5.")
        m = 5
    else:
        try:
            m = int(sys.argv[1])
        except ValueError:
            print("Error: m must be an integer.", file=sys.stderr)
            sys.exit(-1)

    if m < 2 or m > 12:
        print("Error: m out of range, must be between 2 and 12", file=sys.stderr)
        sys.exit(-1)

    # 2. Initialization
    print(f"Initializing RGB image buffer ({NX}x{NY}) and generating points...")
    # UPDATE: Create an RGB array (3 color channels) initialized to White (255)
    image_buffer = np.full((NY, NX, 3), 255, dtype=np.uint8)
    
    a = [math.cos(2 * math.pi * i / m) for i in range(m)]
    b = [math.sin(2 * math.pi * i / m) for i in range(m)]
    
    r = math.sqrt(1.25 * m)
    x, y = 1.0, 1.0
    
    start_time = time.time()
    
    # 3. Escape-Time / Chaos Game Iteration
    for n in range(N):
        if n % (N // 100) == 0:
            percent = (n / N) * 100
            print(f"Progress: {percent:.0f}%", file=sys.stderr)
            
        c = random.randrange(m)
        
        ra = math.sqrt(3.0 * (x*x + y*y))
        if ra == 0: 
            ra = 1e-10 
            
        x1 = -x / r + y / (ra * r) + a[c]
        y1 = -x / (ra * r) - y / r + b[c]
        
        x, y = x1, y1
        
        if n < 100:
            continue
            
        ix = int(x * SCALE + NX / 2)
        iy = int(y * SCALE + NY / 2)

        if 0 <= ix < NX and 0 <= iy < NY:
            # UPDATE: Set the pixel to pure RED (R=255, G=0, B=0)
            image_buffer[iy, ix] = [255, 0, 0]  
            
    print(f"Calculation complete in {time.time() - start_time:.2f} seconds.", file=sys.stderr)

    # 5. Save the image to a PDF file
    fname = "Twon_Dragon.pdf"
    print(f"Saving to {fname}...", file=sys.stderr)
    
    # UPDATE: Use 'RGB' mode to preserve the red color
    img = Image.fromarray(image_buffer, mode='RGB') 
    img.save(fname, format="PDF")
    print("Done.", file=sys.stderr)

if __name__ == "__main__":
    main()