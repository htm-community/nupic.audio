#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2018-2019, Numenta, Inc.  Unless you have an agreement
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

from nupic.data import SENTINEL_VALUE_FOR_MISSING_DATA
from nupic.encoders.base import Encoder

import thorns
import cochlea


class CochleaEncoder(Encoder):
  def __init__(self, fs=100e3, anfs=(60, 25, 15),
               min_cf=125, max_cf=4000, num_cf=2048,
               normalizeInput=True):
    """
    The `CochleaEncoder` encodes an input signal into spike trains of
    auditory nerve fibers.

    It uses the cochlea Python package - https://github.com/mrkrd/cochlea

    Which contains state-of-the-art biophysical models, and gives realistic
    approximation of the auditory nerve activity for a collection of inner
    ear models.

    Auditory nerve fibres have spontaneous rates that vary from 0 to more
    than 120 spikes per second. Fibres with the highest rates of spontaneous
    activity have the lowest thresholds. Once the level of a sound exceeds
    the fibre’s threshold the discharge rate of the fibre rises above its
    spontaneous rate. Eventually, when the sound is made sufficiently high
    in level the fibre cannot fire any faster and reaches saturated discharge
    rate. For high spontaneous rate fibres the shape the function relating
    firing rate to sound levels is sigmoidal whereas for medium and low
    spontaneous rate fibres it may deviate from this and even be straight
    over wide ranges of level. The range over which a fibre changes its
    discharge rate to signal sound level changes is called the dynamic range.
    The dynamic range is narrow for high spontaneous rate fibres and wider
    for medium and low spontaneous rate fibres.
    Source: The basic physiology of the auditory nerve.
            Alan R. Palmer, MRC Institute of Hearing Research

    The spontaneous rate (SR) of discharge varies a lot from one large
    myelinated type I Spiral Ganglion Neuron (SGN) to another and depends
    on certain molecular characteristics. Three categories of SGN have
    been described depending on their SR:
    - low-SR (less than 0.5 spike/sec), about 15% of the SGNs, all forming
      synapses on the modiolar side of the IHC.
    - high-SR (over 18 spikes/sec), about 60% of the SGNs, forming synapses
      on the tunnel pillar side of the IHC.
    - in-between, an intermediate class called medium-SR represents about
      25% of the SGN population.
    Source: http://www.cochlea.eu/en/spiral-ganglion/type-i-sgns-physiology

    The lower limit for the number of characteristic frequencies is 2048.

    A default voice band is used for characteristic frequencies.
    Source: https://en.wikipedia.org/wiki/Voice_frequency

    :param fs: (int) Sampling frequency, in Hertz.
      Defaults to 100e3. Range is [100e3, 500e3].

    :param anfs: (int tuple) Number of auditory nerve fibers.
      (High, Medium, Low) spontaneous rate fiber counts.
      Defaults to (60, 25, 15).

    :param min_cf: (int) Minimum characteristic frequency.
      Defaults to 125. Minimum value is 125.

    :param max_cf: (int) Maximum characteristic frequency.
      Defaults to 4000. Maximum value is 20e3.

    :param normalizeInput: (bool) Whether to normalize input data range to [-1,1]
      Defaults to True.
    """

    # Sampling frequency of the input data.
    self.fs = fs

    # Number of auditory nerve fibers.
    self.anfs = anfs

    # Minimum and maximum characteristic frequency range.
    self.min_cf = min_cf
    self.max_cf = max_cf

    # Number of characteristic frequencies.
    self.num_cf = num_cf

    # Enforce a lower limit for the number of characteristic frequencies.
    if self.num_cf < 2048:
      self.num_cf = 2048

    self.outputWidth = self.num_cf

    if self.max_cf - self.min_cf < self.num_cf:
      self.max_cf = self.min_cf + self.num_cf

    self.normalizeInput = normalizeInput

  def getWidth(self):
    """
    Return the output width, in bits.

    :return outputWidth:  (int) output width
    """
    return self.outputWidth

  def encodeIntoArray(self, inputData, output):
    """
    Encodes inputData and puts the encoded value into the numpy output array,
    which is a 1D array of length returned by getWidth().

    :param inputData: (np.array) Data to encode.
    :param output: (np.array) 1D array. Encoder output.
    """
    pass

  def encodeIntoNeurogram(self, inputData):
    """
    Encodes inputData and returns the encoded neurogram.

    :param inputData: (np.array) Data to encode.
    """

    if type(inputData) != np.ndarray:
      raise TypeError('Expected inputData to be a numpy array but the input '
                      'type is %s' % type(inputData))

    # The Zilany2014 model requires the data to be in dB SPL (deciBel Sound
    # Pressure Level). To do this the auditory threshold is used as the
    # reference sound pressure, i.e. p0 = 20 µPa

    # Desired level of the output signal in dB SPL set to 50
    data = cochlea.set_dbspl(inputData, 50)

    if self.normalizeInput:
      data = np.array([float(val) / pow(2, 15) for val in data])

    # Run model
    anf = cochlea.run_zilany2014(
      data,
      self.fs,
      anf_num=self.anfs,
      cf=(self.min_cf, self.max_cf, self.num_cf),
      seed=0,
      powerlaw='approximate',
      species='human',
    )

    # Accumulate spike trains
    anf_acc = thorns.accumulate(anf, keep=['cf', 'duration'])

    # Sort according to characteristic frequency
    anf_acc.sort_values('cf', ascending=False, inplace=True)

    # Create an array where each row contains a column per characteristic frequency,
    # containing a count of firings (num_cf column count)
    neurogram = thorns.spikes.trains_to_array(anf_acc, self.fs)

    # Clamp multiple spikes to 1
    neurogram = (neurogram > 0) * neurogram

    return neurogram

  def write(self, proto):
    pass
