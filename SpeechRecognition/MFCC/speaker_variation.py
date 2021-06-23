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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yaml
import timeit
import random
import datetime
import random

# Python implementations
# from nupic.algorithms.spatial_pooler import SpatialPooler
# from nupic.algorithms.temporal_memory import TemporalMemory
# from nupic.algorithms.sdr_classifier import SDRClassifier

# C++ implementations
from nupic.bindings.algorithms import SpatialPooler
from nupic.bindings.algorithms import TemporalMemory
from nupic.bindings.algorithms import SDRClassifier

from WavToSDR import WavToSDR


if __name__ == "__main__":

  random.seed(42)
  np.random.seed(42)

  total_time = timeit.default_timer()

  data_path = "../free-spoken-digit-dataset/recordings/"

  verbose = True

  count = 0

  fs = 100e3  # Hz

  encoding_width = 8192  # bits

  with open("../model.yaml", "r") as f:
    modelParams = yaml.safe_load(f)["modelParams"]

    spParams = modelParams["spParams"]
    tmParams = modelParams["tmParams"]
    clParams = modelParams["clParams"]

  sp = SpatialPooler(
    inputDimensions=(encoding_width,),
    columnDimensions=(spParams["columnCount"],),
    potentialPct=spParams["potentialPct"],
    potentialRadius=encoding_width,
    globalInhibition=spParams["globalInhibition"],
    localAreaDensity=spParams["localAreaDensity"],
    numActiveColumnsPerInhArea=spParams["numActiveColumnsPerInhArea"],
    synPermInactiveDec=spParams["synPermInactiveDec"],
    synPermActiveInc=spParams["synPermActiveInc"],
    synPermConnected=spParams["synPermConnected"],
    boostStrength=spParams["boostStrength"],
    seed=spParams["seed"],
    wrapAround=True
  )

  tm = TemporalMemory(
    columnDimensions=(tmParams["columnCount"],),
    cellsPerColumn=tmParams["cellsPerColumn"],
    activationThreshold=tmParams["activationThreshold"],
    initialPermanence=tmParams["initialPerm"],
    connectedPermanence=spParams["synPermConnected"],
    minThreshold=tmParams["minThreshold"],
    maxNewSynapseCount=tmParams["newSynapseCount"],
    permanenceIncrement=tmParams["permanenceInc"],
    permanenceDecrement=tmParams["permanenceDec"],
    predictedSegmentDecrement=0.0,
    maxSegmentsPerCell=tmParams["maxSegmentsPerCell"],
    maxSynapsesPerSegment=tmParams["maxSynapsesPerSegment"],
    seed=tmParams["seed"]
  )

  cl = SDRClassifier([1], 0.001, 0.3, 0)

  # Create an array to represent active columns, all initially zero
  activeColumns = np.zeros(spParams["columnCount"]).astype('uint32')

  training_count = 32

  file_names = []

  # Train with 6 variations of spoken speech
  for j in range(0, training_count):
    file_names.append(data_path + "0_jackson_{}.wav".format(random.randint(0, 5)))
    file_names.append(data_path + "1_jackson_{}.wav".format(random.randint(0, 5)))
    file_names.append(data_path + "2_jackson_{}.wav".format(random.randint(0, 5)))
    file_names.append(data_path + "3_jackson_{}.wav".format(random.randint(0, 5)))

  random.shuffle(file_names)

  # Take into account duplication of samples
  training_count *= 4

  for i, file_name in enumerate(file_names):

    bucketIdx = int(file_name[len(data_path)])

    encoding = WavToSDR(file_name, fs)

    tm.reset()

    print("Training (#{}/{}): {} ({} SDRs)".format(
      i + 1, training_count, file_name, len(encoding)))

    start_time = timeit.default_timer()

    for sdr in encoding:
      # Execute Spatial Pooling algorithm over input space.
      sp.compute(sdr, True, activeColumns)
      activeColumnIndices = np.nonzero(activeColumns)[0]

      # Execute Temporal Memory algorithm over active mini-columns.
      tm.compute(activeColumnIndices, learn=True)
      activeCells = tm.getActiveCells()

      # Run classifier to translate active cells back to scalar value.
      result = cl.compute(
        recordNum=count,
        patternNZ=activeCells,
        classification={
          "bucketIdx": bucketIdx,
          "actValue": bucketIdx
        },
        learn=True,
        infer=False
      )

      count += 1

  # Test the classifier with four unheard "One" variations
  test_names = []
  test_names.append(data_path + "1_jackson_6.wav")
  test_names.append(data_path + "1_jackson_7.wav")
  test_names.append(data_path + "1_jackson_8.wav")
  test_names.append(data_path + "1_jackson_9.wav")

  average_predictions = [[], [], [], []]

  for test_name in test_names:

    bucketIdx = int(test_name[len(data_path)])

    encoding = WavToSDR(test_name, fs)

    print("Testing: {} ({} SDRs)".format(test_name, len(encoding)))

    tm.reset()

    results = []

    start_time = timeit.default_timer()

    for sdr in encoding:
      # Execute Spatial Pooling algorithm over input space.
      sp.compute(sdr, False, activeColumns)
      activeColumnIndices = np.nonzero(activeColumns)[0]

      # Execute Temporal Memory algorithm over active mini-columns.
      tm.compute(activeColumnIndices, learn=False)
      activeCells = tm.getActiveCells()

      # Run classifier to translate active cells back to scalar value.
      result = cl.compute(
        recordNum=count,
        patternNZ=activeCells,
        classification={
          "bucketIdx": bucketIdx,
          "actValue": bucketIdx
        },
        learn=False,
        infer=True
      )

      results.append(result)

      count += 1

    averages = [0, 0, 0, 0]

    for i in range(0, 4):
      for result in results:
        averages[i] += result[1][i]

      averages[i] /= len(results)
      averages[i] *= 100.0

      average_predictions[i].append(averages[i])

    print("Average: {}".format(averages[1]))

  fig, ax = plt.subplots()

  index = np.arange(4)
  bar_width = 0.15

  rects1 = ax.bar(index + (0 * bar_width), average_predictions[0], bar_width, color='r', label='Zero')
  rects2 = ax.bar(index + (1 * bar_width), average_predictions[1], bar_width, color='g', label='One')
  rects3 = ax.bar(index + (2 * bar_width), average_predictions[2], bar_width, color='b', label='Two')
  rects4 = ax.bar(index + (3 * bar_width), average_predictions[3], bar_width, color='k', label='Three')

  ax.set_title('Speaker Variation')
  ax.set_xlabel('Variations')
  ax.set_ylabel('Percentage %')
  ax.set_ylim(0.0, 100.0)
  ax.yaxis.set_major_formatter(mtick.PercentFormatter())
  ax.set_xticks(index + (bar_width * 4) / 2)
  ax.set_xticklabels(('6', '7', '8', '9'))
  ax.legend()

  fig.tight_layout()
  plt.show()

  print("Total time: {}, ({} total SDRs)".format(
    str(datetime.timedelta(seconds=(timeit.default_timer() - total_time))), count))

