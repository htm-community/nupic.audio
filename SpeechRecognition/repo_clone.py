#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: GitPython requires git being installed on the system,
#       and accessible via the system's PATH.
from git import Repo, RemoteProgress

# Echos Git output to stdout
class Progress(RemoteProgress):
    def line_dropped(self, line):
        print line
    def update(self, *args):
        print self._cur_line


# FFSD dataset: 
# A simple audio/speech dataset consisting of recordings of spoken digits in 
# wav files at 8kHz. The recordings are trimmed so that they have near minimal 
# silence at the beginnings and ends.
# 3 speakers
# 1,500 recordings (50 of each digit per speaker)
# English pronunciations
Repo.clone_from(
    "https://github.com/Jakobovski/free-spoken-digit-dataset.git",
    "free-spoken-digit-dataset",
    progress=Progress())


# FrequencyEncoder:
# The FrequencyEncoder encodes a time series chunk (or any 1D array of numeric values)
# by taking the power spectrum of the signal and discretizing it. 
# The maximum amplitude of the power spectrum in this frequency bin is encoded 
# by a ScalarEncoder into an Sparse Distributed Representation (SDR).
Repo.clone_from(
    "https://github.com/marionleborgne/frequency-encoder.git",
    "frequency-encoder",
    progress=Progress())

open("frequency-encoder/__init__.py", 'a').close()
