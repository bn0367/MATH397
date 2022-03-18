gswin64c -q -dBATCH -dNOSAFER -dNOPAUSE -sDEVICE=png256 -sOutputFile=frames/frame%%ld.png rotating_square.eps
ffmpeg -f image2 -framerate 15 -i frames/frame%%d.png -y gol.gif
del "frames\*.png"