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

"""
To use ScalarEncoder on the power spectrum of unpredictable sound chunks, we
need an estimate of the maximum possible value that will occur in any of
these power spectra.

This scripts plots the frequency of the power spectra max values for
different chunk sizes.
"""
from __future__ import division, print_function, absolute_import

import sys
sys.path.append("../frequency-encoder")

from frequency_encoder import FrequencyEncoder, getFreqs

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import scipy.signal as dsp
import thorns as th


def main():
    window_size = 1024
    overlap_factor = 0.5
    symmetric_hann = False
    highlight_chunks = True

    fs = 100e3  # Sampling frequency, Hz

    t = np.arange(0, 0.1, 1 / fs)

    # Make chirp, starting at 125Hz and ramp up to 1000Hz
    data = dsp.chirp(t, 125, t[-1], 1000, method='linear')

    fs = 100e3  # Sampling frequency, Hz

    t = np.arange(0, 0.1, 1 / fs)

    # Make chirp, starting at 125Hz and ramp up to 1000Hz
    data = dsp.chirp(t, 125, t[-1], 1000, method='linear')

    if symmetric_hann:
        # "symmetric" Hann window
        window = np.hanning(window_size)
    else:
        # or, "periodic" Hann window
        window = 0.5 - (0.5 * np.cos(2 * np.pi / window_size * np.arange(window_size)))

    # hop size determines by how many samples the window is advanced
    hop_size = window_size - int(overlap_factor * window_size)

    # pad with zeros to ensure last window fits signal
    padded_samples = np.append(data, np.zeros((len(data) - window_size) % hop_size))

    num_chunks = ((len(padded_samples) - window_size) // hop_size) + 1

    chunks = [padded_samples[i * hop_size:i * hop_size + window_size] * window
              for i in range(num_chunks)]

    print("Min {}, Max {}".format(np.min(chunks), np.max(chunks)))

    numFrequencyBins = 64
    freqBinN = 32
    freqBinW = 9
    minval = 0.0
    maxval = 14.0

    sineEncoder = FrequencyEncoder(numFrequencyBins, freqBinN, freqBinW, minval, maxval)

    encoding = []
    for chunk in chunks:
        encoded = sineEncoder.encode(chunk)
        encoding.append(encoded)

    num_sdr_shown = 18

    ax = []
    ax.append(plt.subplot2grid((2, num_sdr_shown), (0, 0), colspan=num_sdr_shown))

    for i in range(num_sdr_shown):
        ax.append(plt.subplot2grid((2, num_sdr_shown), (1, i)))

    plt.suptitle('Chirp frequency encoding')

    # Plot original signal
    th.plot_signal(
        signal=data,
        fs=fs,
        ax=ax[0],
        color='y'
    )

    if highlight_chunks:
        for i in range(num_chunks):
            offset = 0.0 if not i % 2 else 0.01 * i

            # Create a Rectangle patch
            rect = patches.Rectangle(
                ((i * hop_size)/fs, 1 + offset), window_size/fs, -2 - (offset * 2),
                linewidth=1, edgecolor='r' if not i % 2 else 'b', facecolor='none')

            # Add the patch to the Axes
            ax[0].add_patch(rect)

    ratio = 0.5

    for i in range(num_sdr_shown):
        flipped = np.array(encoding[i]).T
        ax[i+1].imshow(np.reshape(flipped, (-1, 2)), cmap='Greys')

        ax[i+1].set_xticks([])
        ax[i+1].set_yticks([])

        ax[i+1].set_aspect(1.0 / ax[i+1].get_data_ratio() * ratio)

        offset = 0.0 if not i % 2 else 0.05
        con = patches.ConnectionPatch(xyA=(i * hop_size/fs, -1 - offset), xyB=(0, 0.5),
                                      coordsA="data", coordsB="data",
                                      axesA=ax[0], axesB=ax[i+1], arrowstyle="->")
        ax[0].add_artist(con)


    plt.show()


if __name__ == "__main__":
    main()
