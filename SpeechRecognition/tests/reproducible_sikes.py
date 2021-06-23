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

from nupic.encoders.base import Encoder
from nupic.encoders.scalar import ScalarEncoder

from scipy.io import wavfile
import numpy as np
import unittest
import wave
import struct
import sys

import thorns as th
import cochlea


data_dir = "../free-spoken-digit-dataset/recordings"

def show_wav_info(aname, a):
    print("Array", aname)
    print("shape:", a.shape)
    print("dtype:", a.dtype)
    print("min, max:", a.min(), a.max())
    print()


def read_wav_file(file_name):
    _, data = wavfile.read(data_dir + file_name)
    #show_wav_info(file_name, data)
    return data


class TestSpikingEncoding(unittest.TestCase):
  def setUp(self):
    self.data0 = read_wav_file('/0_jackson_0.wav')
    self.data1 = read_wav_file('/0_jackson_1.wav')
    
    # Rescale to [0 .. 1]
    self.data0 = np.array([float(val) / pow(2, 15) for val in self.data0])
    self.data1 = np.array([float(val) / pow(2, 15) for val in self.data1])

    self.minval = 0
    self.maxval = 20.0
    self.fs = 8000  # Hz
    
    # Rescale to [0 .. maxval]
    self.data0 *= self.maxval
    self.data1 *= self.maxval

    # Run model
    self.anf = cochlea.run_zilany2014(
        self.data0,
        self.fs,
        anf_num=(60, 25, 15),
        cf=(125, 4000, 100),
        seed=0,
        powerlaw='approximate',
        species='human',
    )

    # Accumulate spike trains
    self.anf_acc = th.accumulate(self.anf, keep=['cf', 'duration'])
    self.anf_acc.sort_values('cf', ascending=False, inplace=True)


  def test_equal_encoding(self):
    encoding1 = self.encoder.encode(self.data0)
    encoding2 = self.encoder.encode(self.data0)

    freqs = getFreqs(self.data0)
    freqBinSize = len(freqs) / self.numFrequencyBins
    pprint(encoding1, self.numFrequencyBins, freqBinSize)

    self.assertEqual(list(encoding1),
                     list(encoding2))


if __name__ == '__main__':
  unittest.main()
