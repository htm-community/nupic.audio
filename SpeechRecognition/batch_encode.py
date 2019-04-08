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

from __future__ import division, print_function, absolute_import

import numpy as np
import scipy.io.wavfile as wav
import resampy
import fnmatch
import os
import sys

sys.path.append("./cochlea-encoder")
from cochlea_encoder import CochleaEncoder

datapath = 'free-spoken-digit-dataset/recordings'


def main():
    overwrite_all = False

    fs = 100e3  # Sampling frequency, Hz

    encoder = CochleaEncoder(normalizeInput=False)

    # matches = []
    # for root, dirnames, filenames in os.walk(datapath):
    #   for filename in fnmatch.filter(filenames, '?_jackson_*.wav'):
    #     matches.append(os.path.join(root, filename))

    matches = []
    matches.append(datapath + "/0_jackson_0.wav")
    matches.append(datapath + "/1_jackson_0.wav")
    matches.append(datapath + "/2_jackson_0.wav")
    matches.append(datapath + "/3_jackson_0.wav")
    matches.append(datapath + "/4_jackson_0.wav")

    for filename in matches:
      print("Encoding wav file: " + filename)

      samplerate, samples = wav.read(filename)

      filename = filename.replace("wav", "ngm")

      if os.path.isfile(filename + ".npy") is False or overwrite_all is True:
        samples = np.array([float(val) / pow(2, 15) for val in samples])

        # Upsample using resampy. Not as good as scikit.resample is but is useable
        # and certainly better than scipy.signal.resample!
        # http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html
        samples = resampy.resample(samples, samplerate, fs)

        neurogram = encoder.encodeIntoNeurogram(samples)

        np.save(filename, neurogram)


if __name__ == "__main__":
    main()
