#!/usr/bin/env python
#
###############################################################################

import argparse
import marsyas
import marsyas_util
import time
import numpy
import cv
from cv_utils import *
import math
#import matplotlib.pyplot as plt

if __name__ == '__main__':
  windowName = 'Spectral analysis using Marsyas and NuPIC'

  parser = argparse.ArgumentParser(description='Spectral analysis using Marsyas, NuPIC, and OpenCV (OpenGL and GLUT optional).')
  parser.add_argument('--fname', dest='File_Name', type=str, default='test.wav', help='Filename from where data will be extracted')
  parser.add_argument('--flen', dest='Window_len', type=int, default=2048, help='Length (samples) of the window for analysis')
  parser.add_argument('--fstep', dest='Window_step', type=int, default=512, help='Step (samples) of the sliding window used for analysis')
  parser.add_argument('--minfreq', dest='Min_freq', type=float, default=110, help='Minimum frequency (Hz) show in the spectrogram')
  parser.add_argument('--maxfreq', dest='Max_freq', type=float, default=8000, help='Maximum frequency (Hz) show in the spectrogram')
  parser.add_argument('--vtime', dest='Visible_Time', type=float, default=5, help='Visible scrolling time (s) frame show')
  parser.add_argument('--zeropad', dest='Zero_padding', type=float, default=1, help='Zero padding factor (the DFT is calculated after zero-padding the input to this times the input length - use 1 for standard DFT)')
  parser.add_argument('--window', dest='Window_Type', type=str, default='Hamming', help='Shape of the window that will be used to calculate the spectrogram; Hamming, Hanning, Triangle, Bartlett, or Blackman')
  parser.add_argument('--spectrum', dest='Spectrum_Type', type=str, default='logmagnitude2', help='Spectrogram type; power, magnitude, decibels, logmagnitude (for 1+log(magnitude*1000), logmagnitude2 (for 1+log10(magnitude)), or powerdensity')

  args = parser.parse_args()

  # The basic functionality is as follows:
  # Source -> Window -> Spectra -> Output
  #
  FileName = args.File_Name

  # These are the parameters we want to set:
  # For the analysis:
  Window_len = 2048   # The number of samples in each analysis window
  Window_step = 256   # The samples step (in samples) between two
                      # consecutive analysis
  Zero_padding = 1    # After windowing, the signal will be zero-padded
                      # to this value times its length
  Min_freq =  110     # (Hz) The minimum frequency that will be analyzed
  Max_freq = 3000     # (Hz) The maximum frequency that will be analyzed

  Visible_time = args.Visible_Time
  Window_type = args.Window_Type
  Spectrum_type = args.Spectrum_Type

  # The following lines will determine the structure of the marsystem
  # See the following to explain why Gain follows Windowing;
  # http://marsology.blogspot.co.uk/2011/11/common-confusion-in-marsyas.html 
  spec_analyzer = \
    ["Series/analysis", \
      ["SoundFileSource/src", \
       "Sum/summation", \
       "ShiftInput/sft", \
       "Windowing/win", \
       "Gain/gain", \
       "Spectrum/spk", \
       "PowerSpectrum/pspk" \
      ] \
    ] 

  net = marsyas_util.create(spec_analyzer)
  snet = marsyas_util.mar_refs(spec_analyzer)

  # This is the configuration for the MarSystem
  net.updControl(snet["src"]+"/mrs_string/filename", FileName)

  nSamples = net.getControl(snet["src"]+"/mrs_natural/size").to_natural()
  fs = net.getControl(snet["src"]+"/mrs_real/osrate").to_real()

  duration = nSamples/fs

  # This will un-normalize the DFT
  net.updControl(snet["gain"]+"/mrs_real/gain", Window_len*1.0);

  net.updControl("mrs_natural/inSamples", Window_step);
  net.updControl("mrs_real/israte", fs);

  net.updControl(snet["sft"]+"/mrs_natural/winSize", Window_len);
  net.updControl(snet["win"]+"/mrs_natural/zeroPadding", Window_len * (Zero_padding-1));

  net.updControl(snet["win"]+"/mrs_string/type", Window_type);
  net.updControl(snet["pspk"]+"/mrs_string/spectrumType", Spectrum_type);

  DFT_SIZE = Window_len * Zero_padding;
  DFT_SIZE_2 = net.getControl(snet["win"]+"/mrs_natural/onSamples").to_natural();

  # The frequency hop for every bin in the DFT
  freq_bin = fs/DFT_SIZE;

  print "Loaded {0}".format(FileName)
  print "Total samples {0}".format(nSamples)
  print "Samples per second {0}".format(fs)
  print "Track size {0} seconds".format(duration)
  print "DFT size {0} (win samples {1})".format(DFT_SIZE, DFT_SIZE_2)
  print "Hop size {0} (freq. per bin)".format(freq_bin)
  print "Showing {0} seconds".format(Visible_time)

  # This is the size of data that will be shown
  minK = int(math.floor(Min_freq/freq_bin))
  maxK = int(math.ceil(Max_freq/freq_bin))
  #print "minK {0}, maxK {1}".format(minK, maxK)

  # Allocate memory for the image
  deltaK = maxK-minK+1

  nTime = int(math.ceil(Visible_time*(fs*1.0/Window_step)))
  #print "nTime {0}, deltaK {1}".format(nTime, deltaK)

  # 2-dimensional array where the columns represent time 
  # and the lines represent frequencies
  Int_Buff = numpy.zeros([deltaK, nTime])
  #mat = cv.CreateMat(nTime, deltaK, cv.CV_32FC1)

  cv.NamedWindow(windowName, cv.CV_WINDOW_NORMAL) #cv.CV_WINDOW_AUTOSIZE
  cv.MoveWindow(windowName, 0, 0)

  out_control = net.getControl("mrs_realvec/processedData")

  print "use Ctrl+C to exit"
  try:
    while 1:
      net.tick()

      # http://marsology.blogspot.co.uk/2012/02/real-time-spectrogram-and-other-audio.html
      out = out_control.to_realvec()
      out = numpy.array(out)
      out = out[minK:maxK+1]

      # Reverse the order of the output array (to treble at top)
      out = out[::-1]

      # Invert
      #out = 1-out
      
      if numpy.max(out) > 0:
        # Normalize output array before stacking
        out = out/numpy.max(out)
      else:
        break

      if numpy.ndim(out) == 1:    # If out is a 1-dimensional array,
        out = numpy.array([out])  # convert it to 2-dimensional array

      Int_Buff = Int_Buff[:,1:]   # Remove first column of Int_Buff

      # Stack arrays in sequence horizontally (column wise)
      Int_Buff = numpy.hstack([Int_Buff,numpy.transpose(out)])

      # Create an identically shaped image to Int_Buff
      im = array2cv(Int_Buff)

      cv.ShowImage(windowName, im)
      cv.WaitKey(10) # ms

  except KeyboardInterrupt:
    #print "Halted!"
    cv.DestroyAllWindows()
    pass

