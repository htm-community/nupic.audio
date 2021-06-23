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

from __future__ import print_function

import sys

sys.path.append("./cochlea-encoder")

from cochlea_encoder import CochleaEncoder

import numpy as np
import scipy.signal as dsp
import unittest


class TestSpikingEncoding(unittest.TestCase):
  def setUp(self):
    # Sampling frequency, Hz
    fs = 100e3

    t = np.arange(0, 0.1, 1/fs)

    # Make chirp, starting at 125Hz and ramp up to 1000Hz
    self.data0 = dsp.chirp(t, 125, t[-1], 1000)

    # Make chirp, starting at 125Hz and ramp up to 10000Hz
    self.data1 = dsp.chirp(t, 125, t[-1], 10000)

    self.encoder = CochleaEncoder()

  def test_equal_encoding(self):
    encoding1 = self.encoder.encode(self.data0)
    encoding2 = self.encoder.encode(self.data0)

    self.assertEqual(list(encoding1[0:2048]), list(encoding2[0:2048]))

  def test_not_equal_encoding(self):
    encoding1 = self.encoder.encode(self.data0)
    encoding2 = self.encoder.encode(self.data1)

    self.assertNotEqual(list(encoding1[0:2048]), list(encoding2[0:2048]))


if __name__ == '__main__':
  unittest.main()
