#! /bin/bash
#
# file: setup.sh
#
# This bash script performs any setup necessary in order to test your
# entry.  It is run only once, before running any other code belonging
# to your entry.

set -e
set -o pipefail

# Remove (or set it to 0) if you are not using Matlab
NEED_MATLAB=1

# Example: compile a C module (viterbi_Schmidt) for Octave
#mkoctfile -mex viterbi_Springer.c

# Example: compile a C module for Matlab
mex viterbi_Springer.c
