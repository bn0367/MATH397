from subprocess import Popen, PIPE, DEVNULL
import os
from tqdm import trange

frames = 1000
file = "frames/current.eps"
random = "[gridsize gridsize mul {rand 2 mod} repeat]"
template = open("rotating_square_template.eps", "r").read()
last = "[]"
for i in trange(frames):
	with open("frames/current.eps", "w") as f:
		f.write(template.format(start=random if i == 0 else last, loopcount=str(i)))
	last = Popen(['gswin64c', '-q', '-dBATCH', '-dNOSAFER', '-dNOPAUSE', '-sDEVICE=pngalpha', '-sOutputFile=frames/frame%03d.png' % i, 'frames/current.eps'], stdout=PIPE).stdout.read().decode()

Popen(
    ["ffmpeg", "-f", "image2", "-framerate", "15", "-i", "frame%03d.png", "-y", "../rotating_square.gif"], cwd="frames/",
    stdout=DEVNULL, stderr=DEVNULL).wait()

Popen("del *.png", shell=True, cwd="frames/").wait()