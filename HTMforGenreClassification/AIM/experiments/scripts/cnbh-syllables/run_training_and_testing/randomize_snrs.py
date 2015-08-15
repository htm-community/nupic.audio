#!/usr/bin/env python
# encoding: utf-8
"""
randomize_snrs.py

Created by Thomas Walters on 2010-11-06.
"""

import sys
import getopt
import re
import random

help_message = '''
Replace a string in each of two files with a string randomly selected from a list.
'''

replacement_strings = ('snr_0dB',
                       'snr_3dB',
                       'snr_6dB',
                       'snr_9dB',
                       'snr_12dB',
                       'snr_15dB',
                       'snr_18dB',
                       'snr_21dB',
                       'snr_24dB',
                       'snr_27dB',
                       'snr_30dB',
                       'snr_33dB',
                       'snr_36dB',
                       'snr_39dB',
                       'snr_42dB',
                       'snr_45dB',
                       'clean')

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hs:f:m:o:p:", ["help", "string_to_replace=", "input_script_file=", "input_mlf=", "output_script_file=", "output_mlf="])
    except getopt.error, msg:
      raise Usage(msg)
  
    # option processing
    string_to_replace = ""
    script_file = ""
    ml_file = ""
    output_script_file = ""
    output_ml_file = ""
    for option, value in opts:
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-s", "--string_to_replace"):
        string_to_replace = value
      if option in ("-f", "--input_script_file"):
        script_file = value
      if option in ("-o", "--outut_script_file"):
        output_script_file = value
      if option in ("-p", "--output_mlf"):
        output_ml_file = value
      if option in ("-m", "--input_mlf"):
        ml_file = value
      
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2
  
  script = open(script_file, 'r')
  mlf = open(ml_file, 'r')
  out_script = open(output_script_file, 'w')
  out_mlf = open(output_ml_file, 'w')
  out_mlf.write(mlf.readline())
  for l in script:
    replacement = random.choice(replacement_strings)
    out_script.write(re.sub(string_to_replace, replacement, l))
    out_mlf.write(re.sub(string_to_replace, replacement, mlf.readline()))
    out_mlf.write(mlf.readline())
    out_mlf.write(mlf.readline())
    out_mlf.write(mlf.readline())
    out_mlf.write(mlf.readline())
    


if __name__ == "__main__":
  sys.exit(main())
