#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2019, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import scipy.io.wavfile as wav

# Ref: https://python-speech-features.readthedocs.io/en/latest/
import python_speech_features as psf


if __name__ == "__main__":

  data_path = "../free-spoken-digit-dataset/recordings/"
  test_name = "1_jackson_0.wav"

  fs, samples = wav.read(data_path + test_name)
  samples = np.array([float(val) / pow(2, 15) for val in samples])

  # Compute log Mel-filterbank energy features from an audio signal.
  # fbe = psf.logfbank(samples, fs)
  # print("Energy features = \n{}".format(fbe[1:3, :]))

  # Compute MFCC features from an audio signal.
  MFCCs = psf.mfcc(samples, samplerate=fs, numcep=16, winfunc=np.hanning)

  data = np.swapaxes(MFCCs, 0, 1)

  mean = np.mean(data)
  stddev = np.std(data)
  ndata = (data - mean) / stddev

  print("MFCC min={}, max={}, mean={}".format(np.min(ndata), np.max(ndata), np.mean(ndata)))

  fig, ax = plt.subplots(3, 1)
  fig.suptitle('Wav to MFCC')

  ax[0].plot(samples)
  # ax[0].set_title('WAV')

  ax[1].get_shared_x_axes().join(ax[1], ax[2])

  ax[1].imshow(ndata, interpolation='nearest', cmap=cm.coolwarm, origin='lower', aspect='auto')
  # ax[1].set_title('MFCC normalized')

  ax[2].plot(MFCCs)
  # ax[2].set_title('MFCC features')

  plt.show()
