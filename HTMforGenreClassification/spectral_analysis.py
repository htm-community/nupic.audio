#!/usr/bin/env python

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
  parser = argparse.ArgumentParser(description='Spectral analysis of audio files.')
  parser.add_argument('--fname', dest='Filename', type=str, default='test.wav', help='Filename from where data will be extracted')
  parser.add_argument('--flen', dest='Window_len', type=int, default=2048, help='Length (samples) of the window for analysis')
  parser.add_argument('--fstep', dest='Window_step', type=int, default=1024, help='Step (samples) of the sliding window used for analysis')
  parser.add_argument('--minfreq', dest='Min_freq', type=float, default=110, help='Minimum frequency (Hz) show in the spectrogram')
  parser.add_argument('--maxfreq', dest='Max_freq', type=float, default=8000, help='Maximum frequency (Hz) show in the spectrogram')
  parser.add_argument('--maxtime', dest='Max_time', type=float, default=9000, help='Maximum time (s) show in the spectrogram')
  parser.add_argument('--zeropad', dest='Zero_padding', type=float, default=1, help='Zero padding factor (the DFT is calculated after zero-padding the input to this times the input length - use 1 for standard DFT)')
  parser.add_argument('--window', dest='WindowType', type=str, default='Hamming', help='Shape of the window that will be used to calculate the spectrogram; Hamming, Hanning, Triangle, Bartlett, Blackman')
  parser.add_argument('--spectrum', dest='SpectrumType', type=str, default='power', help='Spectrogram type; power, magnitude, decibels, logmagnitude (for 1+log(magnitude*1000), logmagnitude2 (for 1+log10(magnitude)), powerdensity')
  args = parser.parse_args()

  # This program will perform real-time spectral analysis.
  # TODO: Put axis indicators in the plots!
  #
  # The basic functionality is as follows:
  # Source -> Window -> Spectra -> Output
  #
  # These are the parameters we want to set:
  # For the analysis:
  Window_len = 1024  # The number of samples in each analysis window
  Window_step = 512  # The step (in samples) between two consecutive analysis
  Zero_padding = 1  # After windowing, the signal will be zero-padded to this value times its length
  Min_freq =  100    # Hz. The minimum frequency that will be analyzed
  Max_freq = 3000    # Hz. The maximum frequency that will be analyzed

  # The following lines will determine the structure of the marsystem
  spec_analyzer = ["Series/analysis", ["SoundFileSource/src",  "ShiftInput/sft", "Windowing/win","Spectrum/spk","PowerSpectrum/pspk"]] 
  net = marsyas_util.create(spec_analyzer)
  snet = marsyas_util.mar_refs(spec_analyzer)

  # This is the configuration for the MarSystem
  net.updControl(snet["src"]+"/mrs_string/filename", args.Filename)
  nSamples = net.getControl(snet["src"]+"/mrs_natural/size").to_natural()
  fs = net.getControl(snet["src"]+"/mrs_real/osrate").to_real()
  dur = nSamples/fs
  net.updControl("mrs_natural/inSamples", Window_step);
  net.updControl("mrs_real/israte", fs);
  net.updControl(snet["sft"]+"/mrs_natural/winSize", Window_len);
  net.updControl(snet["win"]+"/mrs_natural/zeroPadding", Window_len * (Zero_padding-1));
  net.updControl(snet["win"]+"/mrs_string/type", args.WindowType);
  net.updControl(snet["src"]+"/mrs_bool/initAudio", marsyas.MarControlPtr.from_bool(True));
  net.updControl(snet["pspk"]+"/mrs_string/spectrumType", args.SpectrumType);

  # These variables will avoid having to re-calculate stuff
  DFT_SIZE = Window_len * Zero_padding; # This is the size of the DFT
  DFT_SIZE_2 = net.getControl(snet["win"]+"/mrs_natural/onSamples").to_natural();

  # the frequency hop for every frequency bin in the DFT
  freq_bin = fs/DFT_SIZE;

  print "Debug parameters"
  print "DFT length {0} ({1})".format(DFT_SIZE, DFT_SIZE_2)
  print "Hop size ", freq_bin

  # This is the size of data that will be shown
  visible_time = 5; # Seconds
  minK = int(math.floor(Min_freq/freq_bin))
  maxK = int(math.ceil(Max_freq/freq_bin))
  print "minK {0}, maxK {1}".format(minK, maxK)

  # Allocate memory for the image
  deltaK = maxK-minK+1
  nTime = int(math.ceil(visible_time*(fs*1.0/Window_step)))

  Int_Buff = numpy.zeros([deltaK, nTime])
  print "deltaK {0}, nTime {1}".format(deltaK, nTime)

  mat = cv.CreateMat(nTime, deltaK, cv.CV_32FC1)
  cv.NamedWindow("Marsyas Spectral Analysis", cv.CV_WINDOW_AUTOSIZE)

  try:
    while 1:
      net.tick()

      out = net.getControl("mrs_realvec/processedData").to_realvec()
      out = numpy.array(out)
      out = out[minK:maxK+1]
      out = out [::-1]
      
      if numpy.max(out)>0:
        out = out/numpy.max(out)
      else:
        print numpy.max(out)
        break

      if numpy.ndim(out)==1:
        out = numpy.array([out])

      Int_Buff = Int_Buff[:,1:]
      Int_Buff = numpy.hstack([Int_Buff,numpy.transpose(out)])
      im = array2cv(Int_Buff)
      cv.ShowImage("Marsyas Spectral Analysis", im)
      cv.WaitKey(10)

  except KeyboardInterrupt:
    print "Halted!"
    pass

