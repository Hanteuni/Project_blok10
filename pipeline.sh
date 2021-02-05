#!/bin/bash

python pipe_to_hmm_database.py
python hmm_scan.py
python hmmoutput_to_csv.py