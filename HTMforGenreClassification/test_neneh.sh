#!/bin/sh
#

# 30 seconds from track; Neneh Cherry Ft. Gangstarr - Sassy
sfinfo ncherry.wav

#usage: plot_spectrogram.py [-h] [--fname FILENAME] [--flen WINDOW_LEN]
#                           [--fstep WINDOW_STEP] [--minfreq MIN_FREQ]
#                           [--maxfreq MAX_FREQ] [--maxtime MAX_TIME]
#                           [--zeropad ZERO_PADDING] [--width WIDTH]
#                           [--height HEIGHT] [--window WINDOW]
python plot_spectrogram.py \
  --fname ncherry.wav \
  --flen 1024 \
  --fstep 1024 \
  --maxfreq 8000

mv out.png ncherry_spg1.png

# An alternative Marsyas spectrogram
sound2png ncherry.wav out.png -m spectrogram -ws 1024 -hs 1024 -g 1.5

mv out.png ncherry_spg2.png

# Plot the waveform
sound2png ncherry.wav out.png -m waveform

mv out.png ncherry_wave.png
