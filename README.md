# Video Processing with Object Detection and Trajectories

This project performs video processing using OpenCV to track moving objects and their trajectories. During processing, rectangles that wrap around moving objects are extracted from the video and their trajectories are displayed.

## Description

The project uses the following processing stages:

1. Reading a video file.
2. Calculating the difference between frames to extract moving objects.
3. Applying various methods to reduce noise and improve object extraction (such as blurring and thresholding).
4. Extracting and merging rectangles that wrap around moving objects.
5. Displaying the trajectories of these objects on each frame.
6. Saving the processed video to a new file.

