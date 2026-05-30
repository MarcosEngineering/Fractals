# -*- coding: utf-8 -*-
"""
Created on Wed May  3 18:42:30 2023

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
# Create Barnesley Fractal
# 
#----------------------------------------
# Author : Marco Campolo 2026/05/30


import numpy as np
import matplotlib.pyplot as plt

# Define the transformation matrices (A) and translation vectors (B) for f(x) = Ax + B
matrices = [
    np.array([[0.85, 0.04], [-0.04, 0.85]]),
    np.array([[-0.15, 0.28], [0.26, 0.24]]),
    np.array([[0.20, -0.26], [0.23, 0.22]]),
    np.array([[0.00, 0.00], [0.00, 0.16]])
]

vectors = [
    np.array([0.0, 1.6]),
    np.array([0.0, 0.44]),
    np.array([0.0, 1.6]),
    np.array([0.0, 0.0])
]

probabilities = [0.85, 0.07, 0.07, 0.01]

# Initialize
num_points = 1000000
points = np.zeros((num_points, 2))
current_point = np.array([0.0, 0.0])

# Pre-select all the random choices at once for better performance
choices = np.random.choice(len(matrices), size=num_points, p=probabilities)

# Generate points
for i in range(num_points):
    idx = choices[i]
    current_point = matrices[idx] @ current_point + vectors[idx]
    points[i] = current_point

# Plot the fractal
fig, ax = plt.subplots(figsize=(10, 10))
ax.scatter(points[:, 0], points[:, 1], s=0.1, c="green")
ax.axis('off')

plt.savefig('Barnsley_fractal.pdf', format='pdf')
plt.show()