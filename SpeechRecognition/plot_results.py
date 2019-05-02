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


def main():

    training_count = 16
    results = np.load("results_{}x.npy".format(training_count), allow_pickle=True)

    label0 = []
    label1 = []
    label2 = []
    label3 = []

    for result in results:
      label0.append(result[1][0] * 100.0)
      label1.append(result[1][1] * 100.0)
      label2.append(result[1][2] * 100.0)
      label3.append(result[1][3] * 100.0)

    t = np.arange(0, len(results), 1)

    fig, ax = plt.subplots(2, 2)

    fig.suptitle(
      'Classification Predictions\n'
      'Training: {}x four spoken digits, "Zero" to "Three".    '
      'Testing: 1x heard spoken digit, "One".\n'
      'Classification: 0:{:.2f}%, 1:{:.2f}%, 2:{:.2f}%, 3:{:.2f}%'
        .format(training_count,
                np.sum(label0) / len(label0),
                np.sum(label1) / len(label1),
                np.sum(label2) / len(label2),
                np.sum(label3) / len(label3)))

    ax[0][0].plot(t, label0) #, 'r--')
    ax[0][0].set_xlabel('Zero')
    ax[0][0].set_ylabel('Percentage %')

    ax[0][1].plot(t, label1) #, 'g:')
    ax[0][1].set_xlabel('One')
    ax[0][1].set_ylabel('Percentage %')

    ax[1][0].plot(t, label2) #, 'b.')
    ax[1][0].set_xlabel('Two')
    ax[1][0].set_ylabel('Percentage %')

    ax[1][1].plot(t, label3) #, 'k')
    ax[1][1].set_xlabel('Three')
    ax[1][1].set_ylabel('Percentage %')

    plt.show()


if __name__ == "__main__":
    main()
