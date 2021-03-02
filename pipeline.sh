#!/bin/bash

python3.8 pipe_to_hmm_database.py
python3.8 hmm_scan.py
python3.8 hmmoutput_to_csv.py
