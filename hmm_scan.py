"""Dit script zoekt in de hmm databse met behulp van een fasta bestand,
binnen dit fasta bestand staan meerdere sequenties van dit soort
taxonomy

Author: Teuntje Peeters
Date: Date: 23/11/20"""

import os
import subprocess
import sys
# from pipe_to_hmm_database import taxonomy_type --> werkt nog niet
# Geen idee waarom niet, maar andere keer naar kijken. Voor nu deze
# variabele handmatig aanpassen


def search_hmm_database(inputf, outputf, taxonomy_type):
    """Zoek met een fasta file (inputf) in de hmm database naar matches

    :param inputf: str - naam van de input file (fasta file om mee te
    gaan zoeken)
    :param outputf: str - naam van het bestand die de output bevat van
    de search
    :param taxonomy_type: str - type taxonomy
    :return:
    """
    print("Start met zoeken in hmm database")

    # Selecteer de juiste database
    database = "hmm_db/{}/metagenomics_project_hmms.hmm".format(
        taxonomy_type)
    if not os.path.isdir("hmm_db/{}/hmm_scan_searches".format(
            taxonomy_type)):
        cmd = "mkdir -p hmm_db/{}/hmm_scan_searches".format(taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)
    # Ga daadwerkelijk zoeken in de database
    # (als dit nog niet is gedaan)
    if not os.path.isfile("hmm_db/{}/hmm_scan_searches/{}.tblout".\
                                  format(taxonomy_type, outputf)):
           cmd = "hmmscan --max --tblout {}.tblout {} {}".\
               format(outputf, database, inputf)
           e = subprocess.check_call(cmd, shell=True)
           cmd = "mv {}.tblout hmm_db/{}/hmm_scan_searches".\
               format(outputf, taxonomy_type)
           e = subprocess.check_call(cmd, shell=True)

    else:
        print("Dit output bestand bestaat al")

    print("Done :-)")


if __name__ == '__main__':
    # Geef hier de fasta file om mee te gaan zoeken in de hmm database
    fasta_to_search_with = sys.argv[1]

    # Hier zorgen we ervoor dat de taxonomy type hetzelfde is als de aan-
    # van de database: LET OP, als je dus een andere wilt gebruiken zul
    # je deze variabele moeten aanpassen naar de juiste taxonomy type

    taxonomy_type = "class"
    # De file waar de gevonden matches in opgeslagen gaan worden, dus
    # pas deze aan als onderstaande string niet meer overeen komt met
    # jouw data
    gevonden_matches = sys.argv[1]
    # Ga daadwerkelijk zoeken in de database
    search_hmm_database(fasta_to_search_with,
                        gevonden_matches,
                        taxonomy_type)