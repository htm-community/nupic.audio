#!/usr/bin/env python
# encoding: utf-8
"""
gen_hhed_script.py

Created by Thomas Walters on 2010-07-08.
"""

import sys
import getopt


help_message = '''
Generate an HTK HHed script to change the number of means in the output
distribution to num_means for the emitting states of an HMM with
total_hmm_states states
'''


class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hn:s:v", ["help", "num_means=", "total_hmm_states="])
    except getopt.error, msg:
      raise Usage(msg)
  
    # defaults
    num_means = 3
    total_hmm_states = 6
    
    # option processing
    for option, value in opts:
      if option == "-v":
        verbose = True
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-n", "--num_means"):
        num_means = int(value)
      if option in ("-s", "--total_hmm_states"):
        total_hmm_states = int(value)
  
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2

  out_string = ""
  for state in xrange(2, total_hmm_states):
    out_string += ("MU " + str(num_means) + " {*.state[" + str(state) + "].mix} ")
  print out_string

if __name__ == "__main__":
  sys.exit(main())