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
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy.signal as dsp


def main():
    window_size = 1024
    overlap_factor = 0.5
    symmetric_hann = False

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

    num_frames = ((len(padded_samples) - window_size) // hop_size) + 1

    frames = [padded_samples[i * hop_size:i * hop_size + window_size] * window for i in range(num_frames)]

    # Three plots: Signal, Neurogram, Binary spike counts
    fig, ax = plt.subplots(3, 1)

    for i in range(2):  # num_frames):
        offset = 0.0 if not i % 2 else 0.05

        # Create a Rectangle patch
        rect = patches.Rectangle(
            ((i * hop_size), 1 + offset), window_size, -2 - (offset * 2),
            linewidth=1, edgecolor='r' if not i % 2 else 'b', facecolor='none')

        # Add the patch to the Axes
        ax[0].add_patch(rect)

    # Plot original signal
    ax[0].plot(data)
    ax[0].set_title("Red & Blue overlapping windows")

    # Plot windowing function
    ax[1].plot(window)
    ax[1].set_title("Hann window function")

    # Plot middle extracted signal frame * window function
    ax[2].plot(frames[num_frames//2])
    ax[2].set_title("One chunk of data multiplied by Hann window function")

    plt.show()


if __name__ == "__main__":
    main()
