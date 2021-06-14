#!/bin/bash
set -e

python3.8 pipe_to_hmm_database.py
python3.8 discrepantie_filter_V2.py
python3.8 json_to_fasta.py True
python3.8 json_to_fasta.py False
python3.8 hmm_scan.py data/forward.tblout
python3.8 hmm_scan.py data/reverse.tblout
python3.8 parse_hmm_results_v2.py tblout
python3.8 scoring_system_vis.py All_HMM.json ALL_BLAST.json