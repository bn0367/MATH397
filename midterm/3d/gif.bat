gswin64c -dBATCH -dNOSAFER -dNOPAUSE -sDEVICE=png256 -sOutputFile=frames/frame%%ld.png rotating_square.eps
ffmpeg -f image2 -framerate 15 -i frames/frame%%d.png -y gol_glider_gun.gif
del "frames\*.png"