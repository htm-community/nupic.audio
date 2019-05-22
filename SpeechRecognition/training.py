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
import random
import datetime

# Python implementations
from nupic.algorithms.spatial_pooler import SpatialPooler
# from nupic.algorithms.temporal_memory import TemporalMemory
# from nupic.algorithms.sdr_classifier import SDRClassifier

# C++ implementations
# from nupic.bindings.algorithms import SpatialPooler
from nupic.bindings.algorithms import TemporalMemory
from nupic.bindings.algorithms import SDRClassifier

try:
  import capnp
except ImportError:
  capnp = None
if capnp:
  from nupic.proto import TemporalMemoryProto_capnp
  from nupic.proto import SdrClassifier_capnp


if __name__ == "__main__":

  random.seed(42)
  np.random.seed(42)

  total_time = timeit.default_timer()

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

  cl = SDRClassifier([1], 0.001, 0.3, 0)

  # Create an array to represent active columns, all initially zero. This
  # will be populated by the compute method below. It must have the same
  # dimensions as the Spatial Pooler.
  activeColumns = np.zeros(spParams["columnCount"]).astype('uint32')

  verbose = True
  show_timing = True

  # offset_start = 10000
  # chunk_size = 2500

  training_count = 32

  count = 0

  fs = 100e3  # Hz

  datapath = "./free-spoken-digit-dataset/recordings/"

  # Train on four speech samples

  file_names = []

  # Train with 6 variations of spoken speech
  for j in range(0, training_count):
    file_names.append(datapath + "0_jackson_{}.ngm.npy".format(random.randint(0, 5)))
    file_names.append(datapath + "1_jackson_{}.ngm.npy".format(random.randint(0, 5)))
    file_names.append(datapath + "2_jackson_{}.ngm.npy".format(random.randint(0, 5)))
    file_names.append(datapath + "3_jackson_{}.ngm.npy".format(random.randint(0, 5)))

  # Take into account duplication of samples
  training_count *= 4

  random.shuffle(file_names)

  for i, file_name in enumerate(file_names):

    bucketIdx = int(file_name[len(datapath)])

    encoding = np.load(file_name).astype('uint32')
    # encoding = encoding[offset_start:offset_start+chunk_size]

    tm.reset()

    print("Training (#{}/{}): {} ({} SDRs, {:.4f}s)".format(
      i + 1, training_count, file_name, len(encoding), len(encoding) / fs))

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

  # Save out the current state of the Spatial Pooler, Temporal Memory, and SDR Classifier
  print("Saving Spatial Pooler")
  with open("training_{}x.sp".format(training_count//4), "wb") as f1:
    sp.writeToFile(f1)

  if capnp:
    print("Saving Temporal Memory")
    proto = TemporalMemoryProto_capnp.TemporalMemoryProto.new_message()
    tm.write(proto)
    with open("training_{}x.tm".format(training_count//4), "w") as f:
      proto.write(f)

  if capnp:
    print("Saving SDR Classifier")
    proto = SdrClassifier_capnp.SdrClassifierProto.new_message()
    cl.write(proto)
    with open("training_{}x.cl".format(training_count//4), "w") as f:
      proto.write(f)

  print("Total time: {}, ({} total SDRs)".format(
    str(datetime.timedelta(seconds=(timeit.default_timer() - total_time))), count))
