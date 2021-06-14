#!/bin/bash

python3.8 pipe_to_hmm_database.py

python3.8 discrepantie_filter_V2.py 
python3.8 json_to_fasta.py True
python3.8 json_to_fasta.py False
python3.8 hmm_scan.py data/forward.fasta
python3.8 hmm_scan.py data/reverse.fasta
python3.8 hmmoutput_to_csv.py
python3.8 parse_hmm_results.py tblout
python3.8 score_system.py all_hmm all_BLAST
