ffmpeg -f image2 -framerate 30 -i frames/frame_%%03d.png -y %1
del frames/frame_*.png