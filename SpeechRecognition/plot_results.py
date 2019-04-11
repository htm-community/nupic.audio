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

    results = np.load("results.npy")

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

    fig, ax = plt.subplots()

    fig.suptitle(
      'Classification Predictions\n'
      'Training: 8x four spoken digits ("Zero" to "Three")\n'
      'Testing: 1x unheard spoken digit "One"')

    ax.plot(t, label0, 'r--', label='Zero')
    ax.plot(t, label1, 'g:', label='One')
    ax.plot(t, label2, 'b.', label='Two')
    ax.plot(t, label3, 'k', label='Three')

    ax.set_ylabel('Prediction %')

    legend = ax.legend(loc='center right')

    # Put a nicer background color on the legend.
    legend.get_frame().set_facecolor('C0')

    plt.show()


if __name__ == "__main__":
    main()
