#! /bin/bash
#
# file: next.sh
#
# This bash script analyzes the record named in its command-line
# argument ($1), and writes the answer to the file 'answers.txt'.
# This script is run once for each record in the Challenge test set.
#
# The program should print the record name, followed by a comma,
# followed by a 1 (for an abnormal recording), -1 (for a normal
# recording) or 0 (if unsure.)
#
# For example, if invoked as
#    next.sh a0001
# it analyzes record a0001.wav and (assuming the recording is
# considered to be abnormal) writes "a0001,1" to answers.txt.

set -e
set -o pipefail

RECORD=$1

# Example (Matlab)
#matlab -nodisplay -nodisplay -nosplash -r \
#    "try x = challenge('$RECORD'); \
#     f = fopen('answers.txt', 'a'); fprintf(f, '$RECORD,%d\n', x); fclose(f); \
#     catch e; display(getReport(e)); exit(1); end; quit"

# Example (Octave)
octave -q -f --eval \
    "pkg load signal; pkg load statistics;
     x = challenge('$RECORD');
     f = fopen('answers.txt', 'a'); fprintf(f, '$RECORD,%d\n', x); fclose(f)"
