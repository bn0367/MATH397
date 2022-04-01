gswin64c -dBATCH -dNOSAFER -dNOPAUSE -sDEVICE=png256 -sOutputFile=frames/frame%%ld.png -g500x500 test_old.eps
ffmpeg -f image2 -framerate 30 -i frames/frame%%d.png -y paper1.gif
del "frames\*.png"