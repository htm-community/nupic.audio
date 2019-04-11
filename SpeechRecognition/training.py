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
import yaml
import timeit

from nupic.algorithms.sdr_classifier_factory import SDRClassifierFactory
from nupic.algorithms.spatial_pooler import SpatialPooler
from nupic.algorithms.temporal_memory import TemporalMemory


if __name__ == "__main__":

  # Construct the Spatial Pooler, Temporal Memory, and SDR Classifier

  with open("model.yaml", "r") as f:
    modelParams = yaml.safe_load(f)["modelParams"]

    spParams = modelParams["spParams"]
    tmParams = modelParams["tmParams"]
    clParams = modelParams["clParams"]

  encodingWidth = 2048

  sp = SpatialPooler(
    inputDimensions=(encodingWidth,),
    columnDimensions=(spParams["columnCount"],),
    potentialPct=spParams["potentialPct"],
    potentialRadius=encodingWidth,
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

  classifier = SDRClassifierFactory.create([1], 0.01, 0.1, 1)

  verbose = True
  show_timing = True

  offset_start = 10000
  chunk_size = 2000
  training_count = 8

  count = 0

  fs = 100e3  # Hz

  datapath = "./free-spoken-digit-dataset/recordings/"

  # Train on four speech samples

  file_names = []

  file_names.append(datapath + "0_jackson_0.ngm.npy")
  file_names.append(datapath + "1_jackson_0.ngm.npy")
  file_names.append(datapath + "2_jackson_0.ngm.npy")
  file_names.append(datapath + "3_jackson_0.ngm.npy")

  for j in range(0, training_count):
    for i, file_name in enumerate(file_names):

      encoding = np.load(file_name)
      encoding = encoding[offset_start:offset_start+chunk_size]

      tm.reset()

      print("Training (#{}/{}): {} ({} SDRs, {:.4f}s)".format(
        j + 1, training_count, file_name, len(encoding), len(encoding) / fs))

      start_time = timeit.default_timer()

      for sdr in encoding:
        epoch_time = timeit.default_timer()

        # Create an array to represent active columns, all initially zero. This
        # will be populated by the compute method below. It must have the same
        # dimensions as the Spatial Pooler.
        activeColumns = np.zeros(spParams["columnCount"])

        # Execute Spatial Pooling algorithm over input space.
        sp.compute(sdr, True, activeColumns)
        activeColumnIndices = np.nonzero(activeColumns)[0]

        # Execute Temporal Memory algorithm over active mini-columns.
        tm.compute(activeColumnIndices, learn=True)

        activeCells = tm.getActiveCells()

        # Run classifier to translate active cells back to scalar value.
        result = classifier.compute(
          recordNum=count,
          patternNZ=activeCells,
          classification={
            "bucketIdx": i,
            "actValue": sdr
          },
          learn=True,
          infer=False
        )

        count += 1

        if show_timing and (count % 1000) == 0:
          print("Elapsed time: {:.2f}s, ({} total SDRs)".format(timeit.default_timer() - start_time, count))

        # if show_timing:
        #   print("Epoch time: {:.2f}s".format(timeit.default_timer() - epoch_time))

  # Test the classifier on one of the speech samples

  verbose = True

  bucketIdx = 1

  # Use an unheard spoken 'one' sample to test with.
  # file_name = datapath + "1_jackson_1.ngm.npy"

  # Use an unheard spoken 'one' sample to test with.
  file_name = datapath + "1_jackson_0.ngm.npy"

  print("Testing: {}".format(file_name))

  encoding = np.load(file_name)
  encoding = encoding[offset_start:offset_start+chunk_size]

  tm.reset()

  results = []

  for sdr in encoding:
    # Create an array to represent active columns, all initially zero. This
    # will be populated by the compute method below. It must have the same
    # dimensions as the Spatial Pooler.
    activeColumns = np.zeros(spParams["columnCount"])

    # Execute Spatial Pooling algorithm over input space.
    sp.compute(sdr, False, activeColumns)
    activeColumnIndices = np.nonzero(activeColumns)[0]

    # Execute Temporal Memory algorithm over active mini-columns.
    tm.compute(activeColumnIndices, learn=False)

    activeCells = tm.getActiveCells()

    # Run classifier to translate active cells back to scalar value.
    result = classifier.compute(
      recordNum=count,
      patternNZ=activeCells,
      classification={
        "bucketIdx": bucketIdx,
        "actValue": sdr
      },
      learn=False,
      infer=True
    )

    results.append(result)

    if verbose:
      # Prediction for 1 step out for all four categories (zero to three incl.)
      topPredictions = sorted(zip(result[1], result["actualValues"]), reverse=True)[:4]

      for probability, value in topPredictions:
        print("1-step: {:16} ({:4.4}%)".format(value, probability * 100))

    count += 1

  resarr = np.asarray(results)
  np.save("results", resarr)