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

"""Run inner ear model from [Zilany2014]_.

"""

from __future__ import division, print_function, absolute_import

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import resampy
import sys

sys.path.append("../cochlea-encoder")
from cochlea_encoder import CochleaEncoder


def main():
    # Load a speech file
    file_name = "../free-spoken-digit-dataset/recordings/0_jackson_0.wav"

    samplerate, samples = wav.read(file_name)

    # Rescale to [-1, 1]
    samples = np.array([float(val) / pow(2, 15) for val in samples])

    fs = 100e3              # Sampling frequency, Hz

    # Upsample using resampy. Not as good as scikit.resample is but is useable
    # and certainly better than scipy.signal.resample!
    # http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html
    samples = resampy.resample(samples, samplerate, fs)

    anfs = (60, 25, 15)     # Number of auditory nerve fibers (H,M,L)

    min_cf = 125            # Minimum characteristic frequency
    max_cf = 4000           # Maximum characteristic frequency

    num_cf = 64             # Number of characteristic frequencies
    group_size = 4          # Number of adjacent characteristic
                            # frequencies to group together

    encoder = CochleaEncoder(
        normalizeInput=False,
        anfs=anfs,
        num_cf=num_cf * group_size,
        min_cf=min_cf, max_cf=max_cf)

    neurogram = encoder.encodeIntoNeurogram(samples)

    # Stride over group_size and accumulate cell activations
    activations = []

    # Group overlap?
    for row in neurogram:
        index = 0
        cells = []
        for j in range(len(row) // group_size):
            sm = np.add(row[index:index+group_size])
            spikes = np.mean(sm) > 0.25
            cells.append(int(spikes))

        activations.append(cells)


    # Stride over group_size and accumulate cell activations
    # activations = np.zeros((neurogram.shape[0], neurogram.shape[1] // group_size), dtype=np.int64)
    #
    # it = np.nditer(activations, flags=['c_index'], op_flags=['readwrite'])
    # while not it.finished:
    #     index = it.index * group_size
    #     for i in np.arange(group_size):
    #         it[0] += neurogram.item(index + i)
    #     it.iternext()


    # Three plots: Binary spike counts, Sparsity counts
    fig, ax = plt.subplots(2, 1, sharex=True)

    # Title with the number of High, Medium, and Low spontaneous rate fibers used
    fig.suptitle('Zilany (2014) model. Cells: {} HSR, {} MSR, {} LSR'.format(anfs[0], anfs[1], anfs[2]))

    # Artificially colourise high spiking channels
    spikes = np.zeros((neurogram.shape[0], neurogram.shape[1] // group_size, 3))
    spikes[activations <= 0.001] = (0, 0, 0)
    spikes[activations >= 1.0] = (1, 1, 1)
    spikes[activations >= 2.0] = (1, 0, 0)
    spikes[activations >= 3.0] = (0, 1, 0)
    spikes[activations >= 5.0] = (0, 0, 1)
    ax[0].imshow(np.flipud(np.rot90(spikes)), cmap="Greys", aspect="auto")
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Channel number')

    # Calculate number of non-zero frequencies per row of neurogram,
    # and plot as a percentage sparsity of active frequencies
    sparsity = []

    for row in activations:
        sparsity.append((np.count_nonzero(row) / 2048.0) * 100.0)

    ax[1].plot(sparsity)
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Percentage')

    plt.show()


if __name__ == "__main__":
    main()
