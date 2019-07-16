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

import numpy as np
import itertools
import resampy
import scipy.io.wavfile as wav

# Ref: https://python-speech-features.readthedocs.io/en/latest/
import python_speech_features as psf

from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder as RDSE


SDR_cache = dict()


def WavToSDR(file_name, desired_samplerate=8000):
  global SDR_cache
  if SDR_cache.__contains__(file_name):
    return SDR_cache[file_name]

  samplerate, samples = wav.read(file_name)

  if not samplerate == desired_samplerate:
    samples = resampy.resample(samples, samplerate, desired_samplerate)
    samplerate = desired_samplerate

  winlen = 0.0025  # milliseconds
  winstep = (winlen * 2.5) / 10.0

  MFCCs = psf.mfcc(samples, samplerate=samplerate, winlen=winlen, winstep=winstep, numcep=16, nfft=2048, winfunc=np.hanning)

  # Alter the distribution
  mean = np.mean(MFCCs)
  stddev = np.std(MFCCs)
  ndata = (MFCCs - mean) / stddev

  resolution = max(0.001, (np.max(ndata) - np.min(ndata)) / 1024)

  # Fixing n to 256 allows us to use 16 cepstrums (numcep), for
  # a combined total of 4096 input bits to a Spatial Pooler.
  rdse = RDSE(resolution=resolution, n=512, w=21, offset=np.mean(ndata))

  sdrs = []
  for mfcc in ndata:
    combined = []
    for coef in mfcc:
      sdr = np.zeros(rdse.n)
      rdse.encodeIntoArray(coef, sdr)
      combined.append(sdr)

    merged = list(itertools.chain.from_iterable(combined))
    sdrs.append(np.asarray(merged).astype('uint32'))

  SDR_cache[file_name] = sdrs
  return sdrs
