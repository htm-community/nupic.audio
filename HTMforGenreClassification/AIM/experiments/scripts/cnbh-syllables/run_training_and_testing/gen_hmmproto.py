#!/usr/bin/env python
# encoding: utf-8
"""
gen_hmmproto.py

Created by Thomas Walters on 2010-07-08.
"""

import sys
import getopt


help_message = '''
Generate an HTK HMM prototype with an input_size dimensional input and
total_hmm_states total HMM states (including start and end state)
The feature type string can be specified in feature_type
'''


class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hi:s:t:v", ["help", "input_size=", "total_hmm_states=", "feature_type="])
    except getopt.error, msg:
      raise Usage(msg)
  
    # defaults
    input_size = 39
    total_hmm_states = 6
    feature_type = "MFCC_0_D_A"
    
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-i", "--input_size"):
        input_size = int(value)
      if option in ("-s", "--total_hmm_states"):
        total_hmm_states = int(value)
      if option in ("-t", "--feature_type"):
        feature_type = value
  
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2
    
  print "~o<VECSIZE> " + str(input_size) + "<NULLD>" + "<" + feature_type + ">"
  print "~h \"proto\""
  print "<BEGINHMM>"
  print "<NUMSTATES> " + str(total_hmm_states)
  for state in xrange(2, total_hmm_states):
    print "<State> " + str(state)
    print "<Mean>" + str(input_size)
    print "0 " * input_size
    print "<Variance> " + str(input_size)
    print "1.0 " * input_size
  print
  print "<TransP> " + str(total_hmm_states)
  print "0.0 1.0 " + "0.0 " * (total_hmm_states - 2)
  for state in xrange(1, total_hmm_states - 1):
    print ("0.0 " * state) + "0.6 0.4 " + "0.0 " * (total_hmm_states -2 - state)
  print "0.0 " * total_hmm_states
  print "<EndHMM>"

if __name__ == "__main__":
  sys.exit(main())
