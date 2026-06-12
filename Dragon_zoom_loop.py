# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 10:24:21 2026

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
# Create Manderbrot Fractal zoom Video
# 
#----------------------------------------
# Author : Marco Campolo 2026/06/07

import cv2
import os
import re

def assemble_video():
    image_folder = 'dragon_zoom_frames'
    video_name = 'Dragon_zoom_loop.mp4'
    fps = 10  

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda f: int(re.sub(r'\D', '', f) or 0))

    if not images:
        print(f"Error: No PNG images found in '{image_folder}'.")
        return

    # Get target dimensions from the first readable frame
    first_image_path = os.path.join(image_folder, images[0])
    first_frame = cv2.imread(first_image_path)
    
    if first_frame is None:
        print(f"Error: Could not read the first frame: {first_image_path}")
        return
        
    target_height, target_width, _ = first_frame.shape

    # Set up the Video Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, fps, (target_width, target_height))

    # Create the Zoom-Out Sequence
    unzoom_images = images[-2::-1]
    all_frames = images + unzoom_images

    print(f"Target dimensions: {target_width}x{target_height}")
    print(f"Assembling {len(all_frames)} frames at {fps} FPS...")

    # Write frames with safety checks
    for count, image in enumerate(all_frames):
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        
        # 1. Check if the image is corrupt/unreadable
        if frame is None:
            print(f"[!] Warning: Could not read '{image}'. Skipping.")
            continue
            
        # 2. Check and force resize if dimensions don't match perfectly
        current_height, current_width = frame.shape[:2]
        if (current_width, current_height) != (target_width, target_height):
            # print(f"Resizing '{image}' from {current_width}x{current_height} to match.")
            frame = cv2.resize(frame, (target_width, target_height))

        # Write the guaranteed safe frame
        video.write(frame)
        
        if (count + 1) % 50 == 0:
            print(f"Processed {count + 1}/{len(all_frames)} frames...")

    video.release()
    print(f"\nSuccess! Your looping video is saved as: {video_name}")

if __name__ == "__main__":
    assemble_video()