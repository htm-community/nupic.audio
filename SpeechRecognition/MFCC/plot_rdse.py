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

from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder as RDSE


if __name__ == "__main__":

  data_path = "../free-spoken-digit-dataset/recordings/"
  test_name = "1_jackson_0.wav"

  fs, samples = wav.read(data_path + test_name)
  # samples = np.array([float(val) / pow(2, 15) for val in samples])

  # Compute MFCC features from an audio signal.
  MFCCs = psf.mfcc(samples, samplerate=fs, numcep=16, winfunc=np.hanning)

  data = np.swapaxes(MFCCs, 0, 1)

  # Alter the distribution
  mean = np.mean(data)
  stddev = np.std(data)
  ndata = (data - mean) / stddev

  print("MFCC min={}, max={}, mean={}".format(np.min(ndata), np.max(ndata), np.mean(ndata)))

  numBuckets = [int(np.power(2, x)) for x in range(5, 10)]

  data_range = np.arange(np.min(ndata), np.max(ndata), (np.max(ndata) - np.min(ndata)) / 1000)

  fig, ax = plt.subplots(1, len(numBuckets), sharex=True)
  fig.suptitle('RDSE resolution (n=256 bits)\nInput discretized into 1000 values\nNumber of buckets in brackets')

  ax[0].set_ylabel('Bits')

  for i, num in enumerate(numBuckets):
    resolution = max(0.001, (np.max(ndata) - np.min(ndata)) / num)

    # Fixing n to 256 allows us to use 16 cepstrums (numcep), for
    # a combined total of 4096 input bits to a Spatial Pooler.
    rdse = RDSE(resolution=resolution, n=256)

    sdrs = []
    for x in data_range:
      sdr = np.zeros(rdse.n)
      rdse.encodeIntoArray(x, sdr)
      sdrs.append(sdr)

    sdrs = np.swapaxes(sdrs, 0, 1)

    ax[i].imshow(sdrs)
    ax[i].set_title('{0:.4f} ({1})'.format(resolution, num))
    ax[i].set_yticklabels([])

  plt.show()
