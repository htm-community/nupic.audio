#!/usr/bin/python
"""
plot_munged_results.py

"""

import matplotlib as mpl
mpl.use('PDF')
import numpy as np
import pylab as p
#import matplotlib.pyplot as plt

f=open("results_test_all.csv","r")
results = dict()
for line in f:
  if line[0] != "#":
    values = line.strip().split(",")
    results.setdefault(values[3],dict())
    results[values[3]].setdefault(values[0], dict())
    results[values[3]][values[0]].setdefault(values[1], dict())
    results[values[3]][values[0]][values[1]].setdefault(int(values[4]), dict())
    results[values[3]][values[0]][values[1]][int(values[4])].setdefault(int(values[5]), dict())
    results[values[3]][values[0]][values[1]][int(values[4])][int(values[5])].setdefault(int(values[6]), dict())
    if values[2] == 'clean':
       snr = 50
       results[values[3]][values[0]][values[1]][int(values[4])][int(values[5])][int(values[6])][snr] = float(values[7])
    else:
       snr = int(values[2])
       results[values[3]][values[0]][values[1]][int(values[4])][int(values[5])][int(values[6])][snr] = float(values[7])
#    results[values[3]].append((values[1],values[2],values[2],values[4]))

ax = mpl.pyplot.subplot(111)
train_set = 'inner'
for hmm_iterations in [2,3,15]:
  for hmm_states in [3,4]:
    for hmm_components in [3,4]:
      lines = []
      labels = []
      ax.cla()
      for feature_type in ('mfcc', 'mfcc_vtln', 'aim'):
        for feature_subtype in results[train_set][feature_type].keys():
          try:
            this_line = results[train_set][feature_type][feature_subtype][hmm_states][hmm_components][hmm_iterations].items()
            this_line.sort(cmp=lambda x,y: x[0] - y[0])
            xs, ys = zip(*this_line)
            xs = list(xs)
            ys = list(ys)
            line, = ax.plot(xs,ys,'-o',linewidth=2)
            lines.append(line)
            labels.append(feature_type + "_" + feature_subtype)
          except KeyError:
            print "Data not found"
      p.legend(lines, labels, 'upper left', shadow=True)
      p.xlabel('SNR/dB')
      p.ylabel('Recognition performance %')
      output_file = ("recognition_vs_snr_%diterations_%dstates_%d_components.pdf" % (hmm_iterations, hmm_states, hmm_components))
      p.savefig(output_file)