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

"""Run inner ear model from [Zilany2014]_.

"""

from __future__ import division, print_function, absolute_import

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as dsp

import thorns as th
import cochlea


def main():
    fs = 100e3              # Sampling frequency, Hz
    anfs = (60, 25, 15)     # Number of auditory nerve fibers (H,M,L)

    num_cf = 100            # Number of characteristic frequencies
    min_cf = 125            # Minimum characteristic frequency
    max_cf = 4000           # Maximum characteristic frequency

    t = np.arange(0, 0.1, 1/fs)

    # Make chirp, starting at 300Hz and ramp up to 3000Hz
    s = dsp.chirp(t, 300, t[-1], 3000)

    # The Zilany2014 model requires the data to be in dB SPL.
    # To do this the auditory threshold is used as the reference
    # sound pressure, i.e. p0 = 20 µPa
    # Desired level of the output signal in dB SPL set to 50
    data = cochlea.set_dbspl(s, 50)

    # Run model
    anf = cochlea.run_zilany2014(
        data,                           # In Pa
        fs,                             # range [100e3, 500e3]
        anf_num=anfs,                   # (HSR#, MSR#, LSR#)
        cf=(min_cf, max_cf, num_cf),    # cf range [125, 20e3]
        seed=0,
        powerlaw='approximate',
        species='human',
    )

    # Accumulate spike trains
    anf_acc = th.accumulate(anf, keep=['cf', 'duration'])

    # Sort according to characteristic frequency
    anf_acc.sort_values('cf', ascending=False, inplace=True)

    # Three plots: Signal, Neurogram, Binary spike counts
    fig, ax = plt.subplots(3, 1)

    # Title with the number of High, Medium, and Low spontaneous rate fibers used
    fig.suptitle('Zilany (2014) model. Cells: {} HSR, {} MSR, {} LSR'.format(anfs[0], anfs[1], anfs[2]))

    # Plot original signal
    th.plot_signal(
        signal=data,
        fs=fs,
        ax=ax[0]
    )

    # Visualize spike_trains by converting them to bit map
    th.plot_neurogram(
        anf_acc,
        fs,
        ax=ax[1]
    )

    # Create an array where each row contains a column per characteristic frequency,
    # containing a count of firings (num_cf column count)
    neurogram = th.spikes.trains_to_array(anf_acc, fs)

    # Clamp multiple spikes to 1
    # neurogram = (neurogram > 0) * neurogram

    spikes = np.zeros((neurogram.shape[0], neurogram.shape[1], 3))
    spikes[neurogram <= 0.001] = (0, 0, 0)
    spikes[neurogram >= 1.0] = (1, 1, 1)
    spikes[neurogram >= 2.0] = (1, 0, 0)
    spikes[neurogram >= 3.0] = (0, 1, 0)
    spikes[neurogram >= 5.0] = (0, 0, 1)
    plt.imshow(np.flipud(np.rot90(spikes)), cmap="Greys", aspect="auto")
    ax[2].set_xlabel('Time (s)')
    ax[2].set_ylabel('Channel number')

    plt.show()


if __name__ == "__main__":
    main()
