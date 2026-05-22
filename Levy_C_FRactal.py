"""
Created on Wed May 20 20:17:24 2026

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
# Create a Levy C Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/22


from PIL import Image, ImageDraw
import math

# 1. Canvas setup with higher resolution for crisp details
imgx = 2048
imgy = 2048
image = Image.new("RGB", (imgx, imgy), (13, 8, 0)) # Base dark amber color '#0D0800'
draw = ImageDraw.Draw(image)

def levy_c_curve(xa, ya, xb, yb, current_depth, max_depth):
    global draw
    
    # Calculate vector distance
    xd = xb - xa
    yd = yb - ya
    d = math.hypot(xd, yd)
    
    # CRITICAL FIX: Only draw at the base case (final depth or pixel threshold) 
    # to prevent upper layers from painting over the delicate micro-structures.
    if d < 1.5 or current_depth >= max_depth:
        # Dynamically change color by structural depth to match the golden highlight contrast
        # Early depths get antique gold; deep details get brilliant white
        t = current_depth / max_depth
        r = int((1.0 - t) * 139 + t * 255) # Blend from #8B (139) to #FF (255)
        g = int((1.0 - t) * 101 + t * 245) # Blend from #65 (101) to #F5 (245)
        b = int((1.0 - t) * 8   + t * 230) # Blend from #08 (8)   to #E6 (230)
        
        draw.line([(int(xa), int(ya)), (int(xb), int(yb))], fill=(r, g, b), width=1)
        return
        
    # Isosceles right triangle geometry calculation
    x = xa + xd * 0.5 - yd * 0.5
    y = ya + xd * 0.5 + yd * 0.5
    
    # Recurse down into both halves of the new triangle point
    levy_c_curve(xa, ya, x, y, current_depth + 1, max_depth)
    levy_c_curve(x, y, xb, yb, current_depth + 1, max_depth)

# --- Execute Main Sequence ---
print("Generating geometric recursion layers...")
mx = imgx - 1
my = imgy - 1

# Position the starting base line right in the center field
# Max depth of 15-18 provides beautiful, ultra-fine lace lines
levy_c_curve(mx * 0.3, my * 0.65, mx * 0.7, my * 0.65, current_depth=0, max_depth=16)

print("Saving high-contrast geometric fractal visualization...")
image.save("Levy_C_Fractal.pdf", "pdf")
print("Done. Check your folder for 'Levy_C_Fractal.pdf'.")
