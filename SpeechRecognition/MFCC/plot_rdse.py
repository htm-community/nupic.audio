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
import numpy as np
import scipy.io.wavfile as wav
import resampy

# Ref: https://python-speech-features.readthedocs.io/en/latest/
import python_speech_features as psf

from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder as RDSE


if __name__ == "__main__":

  data_path = "../free-spoken-digit-dataset/recordings/"
  test_name = "1_jackson_0.wav"

  fs, samples = wav.read(data_path + test_name)
  samples = np.array([float(val) / pow(2, 15) for val in samples])

  desired_samplerate = 50000

  if not fs == desired_samplerate:
    samples = resampy.resample(samples, fs, desired_samplerate)
    fs = desired_samplerate

  # Compute MFCC features from an audio signal.
  MFCCs = psf.mfcc(samples, samplerate=fs, numcep=16, nfft=2048, winfunc=np.hanning)

  data = np.swapaxes(MFCCs, 0, 1)

  # Alter the distribution
  mean = np.mean(data)
  stddev = np.std(data)
  ndata = (data - mean) / stddev

  print("MFCC min={}, max={}, mean={}".format(np.min(ndata), np.max(ndata), np.mean(ndata)))

  numBuckets = [int(np.power(2, x)) for x in range(7, 12)]

  data_range = np.arange(np.min(ndata), np.max(ndata), (np.max(ndata) - np.min(ndata)) / 1000)

  # Fixing n to 512 allows us to use 16 cepstrums (numcep), for
  # a combined total of 8192 input bits to a Spatial Pooler.
  n = 512
  w = 21

  fig, ax = plt.subplots(1, len(numBuckets), sharex=True)
  fig.suptitle('RDSE resolution (n={} w={})\n\nInput discretized into 1000 values. Number of buckets in brackets'.format(n, w))

  # Alter wspace to spread out subplots
  plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.2)

  ax[0].set_ylabel('Bits')

  for i, num in enumerate(numBuckets):
    resolution = max(0.001, (np.max(data_range) - np.min(data_range)) / num)

    rdse = RDSE(resolution=resolution, n=n, w=w, offset=np.mean(data_range))

    sdrs = []
    for x in data_range:
      sdr = np.zeros(rdse.n)
      rdse.encodeIntoArray(x, sdr)
      sdrs.append(sdr)

    sdrs = np.swapaxes(sdrs, 0, 1)

    ax[i].imshow(sdrs)
    ax[i].set_title('{0:.4f} ({1})'.format(resolution, num))
    ax[i].set_yticklabels([])
    ax[i].set_xticks([0, ax[i].get_xticks()[-1] / 2, ax[i].get_xticks()[-1]])
    ax[i].set_xticklabels(['{:.2f}'.format(np.min(data_range)), '', '{:.2f}'.format(np.max(data_range))])

    print("{} buckets = {}".format(num, rdse))

  plt.show()
