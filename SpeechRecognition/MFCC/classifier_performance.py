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
import yaml
import timeit
import random
import datetime
import itertools
import resampy
import scipy.io.wavfile as wav

# Ref: https://python-speech-features.readthedocs.io/en/latest/
import python_speech_features as psf

from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder as RDSE

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

  # Use an unheard spoken 'one' sample to test with.
  # test_name = "1_jackson_1.wav"

  # Use a heard spoken 'one' sample to test with.
  test_name = "1_jackson_0.wav"

  test_sdrs = WavToSDR(data_path + test_name, 100000)

  verbose = True
  show_timing = False

  count = 0

  encoding_width = 8192  # bits

  # training_counts = [int(np.power(2, x)) for x in range(3, 7)]
  # training_counts = [32, 64, 128, 256, 512]
  training_counts = [2, 4, 8, 16, 32]

  average_predictions = [[], [], [], []]

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

  # Create an array to represent active columns, all initially zero. This
  # will be populated by the compute method below. It must have the same
  # dimensions as the Spatial Pooler.
  activeColumns = np.zeros(spParams["columnCount"]).astype('uint32')

  for training_count in training_counts:

    file_names = []

    for j in range(0, training_count):
      file_names.append(data_path + "0_jackson_0.wav")
      file_names.append(data_path + "1_jackson_0.wav")
      file_names.append(data_path + "2_jackson_0.wav")
      file_names.append(data_path + "3_jackson_0.wav")

    random.shuffle(file_names)

    # Take into account duplication of samples
    training_count *= 4

    if count > 0:
      # Discount for existing training of the SP, TM, and CL
      training_count //= 2

      file_names = np.array(file_names)
      file_names.resize(training_count, refcheck=False)

    for i, file_name in enumerate(file_names):

      bucketIdx = int(file_name[len(data_path)])

      encoding = WavToSDR(file_name, 100000)

      tm.reset()

      print("Training (#{}/{}): {} ({} SDRs)".format(
        i + 1, training_count, file_name, len(encoding)))

      start_time = timeit.default_timer()

      for sdr in encoding:
        # if show_timing:
        #   epoch_time = timeit.default_timer()

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

        if show_timing and (count % 1000) == 0:
          print("Elapsed time: {}, ({} total SDRs)".format(
            str(datetime.timedelta(seconds=(timeit.default_timer() - start_time))), count))

        # if show_timing:
        #   print("Epoch time: {:.2f}s".format(timeit.default_timer() - epoch_time))

    # with open("training_{}x.sp.pkl".format(training_count//4), "wb") as f1:
    #   sp.writeToFile(f1)
    # with open("training_{}x.tm.pkl".format(training_count//4), "wb") as f2:
    #   tm.writeToFile(f2)
    # with open("training_{}x.cl.pkl".format(training_count//4), "wb") as f3:
    #   cl.writeToFile(f3)

    # Test the classifier
    file_name = data_path + test_name

    bucketIdx = int(file_name[len(data_path)])

    encoding = WavToSDR(file_name, 100000)

    print("Testing: {} ({} SDRs)".format(
      file_name, len(encoding)))

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

      if show_timing and (count % 1000) == 0:
        print("Elapsed time: {}, ({} total SDRs)".format(
          str(datetime.timedelta(seconds=(timeit.default_timer() - start_time))), count))

      # if verbose:
      #   # Prediction for 1 step out for all four categories (zero to three incl.)
      #   topPredictions = sorted(zip(result[1], result["actualValues"]), reverse=True)[:4]
      #
      #   for probability, value in topPredictions:
      #     print("1-step: {:16} ({:4.4}%)".format(value, probability * 100))

    # resarr = np.asarray(results)
    # np.save("results_{}x".format(training_count//4), resarr)

    averages = [0, 0, 0, 0]
    percentages = [0, 0, 0, 0]

    for i in range(0, 4):
      for result in results:
        averages[i] += result[1][i]

      averages[i] /= len(results)
      averages[i] *= 100.0

      percentages[i] = averages[i]

      average_predictions[i].append(percentages[i])

    print("Average: {}".format(averages[1]))

  fig, ax = plt.subplots()

  index = np.arange(len(training_counts))
  bar_width = 0.15

  rects1 = ax.bar(index + (0 * bar_width), average_predictions[0], bar_width, color='r', label='Zero')
  rects2 = ax.bar(index + (1 * bar_width), average_predictions[1], bar_width, color='g', label='One')
  rects3 = ax.bar(index + (2 * bar_width), average_predictions[2], bar_width, color='b', label='Two')
  rects4 = ax.bar(index + (3 * bar_width), average_predictions[3], bar_width, color='k', label='Three')

  ax.set_title('Classifier Performance')
  ax.set_xlabel('Count')
  ax.set_ylabel('Percentage %')
  ax.set_xticks(index + (bar_width * 4) / 2)
  ax.set_xticklabels(tuple(training_counts))
  ax.legend()

  fig.tight_layout()
  plt.show()

  print("Total time: {}, ({} total SDRs)".format(
    str(datetime.timedelta(seconds=(timeit.default_timer() - total_time))), count))
