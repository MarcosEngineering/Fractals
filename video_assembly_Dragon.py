# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 08:20:46 2026

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
# Create a Dragon_Julia Fractal Zoom Video
# 
#----------------------------------------
# Author : Marco Campolo 2026/06/06

import cv2
import os

def assemble_video():
    # --- Configuration ---
    image_folder = 'dragon_zoom_frames_Origin_Spark'
    video_name = 'dragon_zoom_animation.mp4'
    fps = 12  # Frames per second 

    # 1. Gather and sort the images
    # We sort them to ensure frame_000 comes before frame_001, etc.
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()

    if not images:
        print(f"Error: No PNG images found in the '{image_folder}' folder.")
        return

    # 2. Get the dimensions from the very first frame
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, layers = frame.shape

    # 3. Set up the Video Writer
    # 'mp4v' is the standard codec for creating .mp4 files in OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    print(f"Found {len(images)} frames. Assembling video at {fps} FPS...")

    # 4. Loop through the images and write them to the video file
    for count, image in enumerate(images):
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
        
        # Optional: Print progress every 25 frames
        if (count + 1) % 25 == 0:
            print(f"Processed {count + 1}/{len(images)} frames...")

    # 5. Clean up and finalize the file
    video.release()
    print(f"\nSuccess! Your video is saved as: {video_name}")

if __name__ == "__main__":
    assemble_video()