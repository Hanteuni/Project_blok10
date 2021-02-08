#!/bin/bash

python3.8 "pipe_to_hmm_database.py"
echo piped
python3.8 "hmm_scan.py"
echo scanned
python3.8 "hmmoutput_to_csv.py"
echo dun