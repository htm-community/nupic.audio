#!/bin/bash
find ./ -iname "*.txt" | xargs grep "Score on test talkers" | sed "s/\.\///" | sed "s/4_states_4_mixture_components\/results_iteration_15.txt:# Score on test talkers: //" | sed "s/\//,/g" | sed "s/dB//" | sed "s/snr_//" | sed "s/_talkers//" | sed s/%// | sed s/,0,/,00,/ | sed s/,3,/,03,/ | sed s/,6,/,06,/ | sed s/,9,/,09,/ > results_test_all.csv
