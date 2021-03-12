"""Deze python code is een pipeline om van het 16s bestand losse
hmms te bouwen per taxonomy, ook kun je de code gebruiken om hier
in te zoeken met hmm scan. De code hmmoutput_to_csv is om de
output hiervan te parsen"""

#Author: Teuntje Peeters
#Date: 23/11/20

from sys import argv
import os
import subprocess


def get_index_taxonomy(file, taxonomy_type):
    """Get index of taxonomy_type om dit te automatiseren

    :param file: str - naam csv bestand
    :param taxonomy_type: str - naam taxonomy
    :return: idx - integer, de index van de taxonomy type
    """
    i = 0
    counter = 0
    # Lees alleen de eerste regel van het bestand
    with open(file) as inFile:
        while i < 1:
            line = inFile.readline().split("\t")
            # Voor iedere kolom checken of de taxonomy voorkomt
            for col in line:
                if taxonomy_type in col:
                    # als de taxonomy in de colom zit returnen we de
                    # counter
                    return counter
                counter += 1
            i+=1


def parse_csv(file, idx):
    """Open en lees het csv bestand in

    Input:
    :param file: - str - naam van het csv bestand
    :param idx: int - index van de taxonomy type waar we in gaan zoeken

    Output:
    output_dict - dict - {>refseq_id_taxonomy:seq, >refseq_id_taxonomy:seq}
    taxo_types - list - alle taxo_types (of categorie waar we nu in zoeken)
    worden hierin opgeslagen
    Dit is eigenlijk gewoon de naam van de taxonomy
    """
    print("Lees het csv bestand in..")
    # declareer variabelen
    output_dict = {}
    taxo_types = []
    # Open en lees het bestand
    with open(file) as inFile:
        next(inFile)
        # voor iedere regel in het bestand de regel splitten op tabs
        # de taxonomy eruit halen (hier een unieke lijst van maken)
        # dictionary maken met een unieke key en organisme met als value
        # de sequentie
        for line in inFile:
            line = line.split("\t")
            if line[idx] == "":
                tt = "unknown"
            else:
                tt = line[idx].split(":")[1]

            if tt not in taxo_types:
                taxo_types.append(tt.replace(" ", "_"))

            refseq_id = line[2]
            seq = line[10]
            output_dict[">{}_{}".format(refseq_id, tt)] = seq
    print("Bestand ingelezen")
    return output_dict, taxo_types


def fasta_writer(csv_dict, taxo_types, taxonomy_type):
    """Maak voor iedere taxonomy een eigen fasta bestand en schrijf deze
    weg in eigen unieke map

    :param csv_dict: dict - {>refseq_id_taxonomy:seq,
    >refseq_id_taxonomy:seq}
    :param taxo_types: - list - unieke taxo_types in het input bestand
    :return: schrijft bestanden weg in corresponderende mappen
    """
    print("Start met het maken van losse folders per taxonomy")
    print("Start met het schrijven van alle fasta files")
    # Maak folders aan per taxonomy in het bestand
    if not os.path.isdir(taxonomy_type):
        cmd = "mkdir -p {}".format(taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)

    for taxonomy in taxo_types:
        taxonomy = taxonomy.strip("\n")
        taxonomy_folder = "{}/{}".format(taxonomy_type, taxonomy)
        if not os.path.isdir(taxonomy_folder):
            cmd = "mkdir -p {}/{}".format(taxonomy_type, taxonomy)
            e = subprocess.check_call(cmd, shell=True)

        # Als het fasta bestand nog niet bestaat maak je deze aan en
        # wordt deze gevuld met het de dna sequenties
        if not os.path.isfile("{}/{}/{}.fasta".format(taxonomy_type, taxonomy_folder, taxonomy)):
            with open("{}/{}.fasta".format(taxonomy_folder, taxonomy),
                      "w") as inFile:
                for key, value in csv_dict.items():
                    if taxonomy in key:
                        inFile.write("{}\n".format(key))
                        inFile.write("{}\n".format(value))


def msa(taxo_types, taxonomy_type):
    """Maak van iedere taxonomy een eigen multiple sequence alignment

    :param taxo_types: list - unieke taxo_types in het input bestand
    :return:
    """
    print("Start met het maken van MSA")
    csv_statistieken = open("{}/statistieken.csv".format(taxonomy_type), "w", encoding="utf-8")
    csv_statistieken.write(taxonomy_type + "," + "aantal" + "\n")
    # Ga over iedere taxonomy heen
    for taxonomy in taxo_types:
        taxonomy = taxonomy.strip("\n")
        taxonomy_folder = "{}/{}".format(taxonomy_type, taxonomy)
        fasta = "{}/{}.fasta".format(taxonomy_folder, taxonomy)
        csv_statistieken.write(str(taxonomy) + "," + str(round(len(open(fasta, "r").readlines())/2)) +"\n")
        # Als het MSA bestand nog niet bestaat en het fasta bestand niet
        # leeg is wordt MAFFT aangeroepen om hier een msa van te maken
        if not os.path.isfile("{}/{}.msa".format(taxonomy_folder, taxonomy)):
            if not os.stat(fasta).st_size == 0:
                cmd = "mafft {} > {}/{}.msa".format(fasta,
                                                            taxonomy_folder,
                                                            taxonomy)
                e = subprocess.check_call(cmd, shell=True)
    csv_statistieken.close()

def build_hmms(taxo_types, taxonomy_type):
    """Bouw van iedere msa een hmm

    :param taxo_types: list - unieke taxo_types in het input bestand
    :return:
    """
    print("Start met het maken van alle hmm per taxonomy")
    for taxonomy in taxo_types:
        taxonomy_folder = "{}/{}".format(taxonomy_type, taxonomy)
        msa = "{}/{}.msa".format(taxonomy_folder, taxonomy)
        # Als het hmm bestand niet bestaat en het msa bestand WEL bestaat
        # wordt er gecheckt of het msa bestand niet leeg is vervolgens
        # wordt hmm build aangeroepen om een hmm te bouwen van deze msa
        if not os.path.isfile("{}/{}.hmm".format(taxonomy_folder, taxonomy)) and\
            os.path.isfile("{}/{}.msa".format(taxonomy_folder, taxonomy)):
            if not os.stat(msa).st_size == 0:
                cmd = "hmmbuild {}/{}.hmm {}".format(taxonomy_folder, taxonomy, msa)
                try:
                    e = subprocess.check_call(cmd, shell=True)
                except:
                    print(msa)


def hmm_db(taxo_types, taxonomy_type):
    """Maak van alle hmms een database om in te kunnen zoeken

    :param taxo_types: list - unieke taxo_types in het input bestand
    :return:
    """
    print("Start met het maken van hmm database")
    # Maak de map met de hmm database aan
    hmm_locations = []
    if not os.path.isdir("hmm_db/{}".format(taxonomy_type)):
        cmd = "mkdir -p hmm_db/{}".format(taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)
    print("done")

    # Verkrijg alle hmm locaties
    for tt in taxo_types:
        tt_folder = "{}/{}".format(taxonomy_type, tt)
        hmm = "{}/{}.hmm".format(tt_folder, tt)
        if os.path.isfile(hmm):
            hmm_locations.append(hmm)

    # Combineer alle hmms in een bestand
    if not os.path.isfile("hmm_db/{}/{}_project_hmms.hmm".format(
            taxonomy_type, taxonomy_type)):
        cmd = "touch hmm_db/{}/metagenomics_project_hmms.hmm".\
            format(taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)
        cmd = "cat {} > hmm_db/{}/metagenomics_project_hmms.hmm".format\
             (" ".join(hmm_locations), taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)

    # Verkrijg de lijst van beschikbare bestanden in de volgende map:
    database_files = os.listdir("hmm_db/{}".format(taxonomy_type))
    counter = 0
    for file in database_files:
        if "h3i" in file or "h3m" in file or "h3f" in file or "h3p" in file:
            counter += 1
    if counter < 4:
        cmd = "hmmpress hmm_db/{}/metagenomics_project_hmms.hmm".format(taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)
    else:
        print("Database al gebouwd")


if __name__ == '__main__':
    # Geef de input file
    file = "data/janne.csv"

    # Met welk taxonomy_type werken we op het moment?
    taxonomy_type = "genus"

    taxonomy_type_idx = get_index_taxonomy(file, taxonomy_type)
    # parse de csv en sla deze op in een dictionary, verkrijg de
    # verschillende taxo_types
    csv_dict, taxo_types = parse_csv(file, taxonomy_type_idx)

    # van iedere taxonomy_type wordt een fasta bestand gemaakt en in de
    # bijbehorende map gezet
    fasta_writer(csv_dict, taxo_types, taxonomy_type)

    # Maak een multiple sequence alignment per taxo_types en plaats deze
    # in de bijbehorende map
    msa(taxo_types, taxonomy_type)

    # Maak een hidden markov mocdel per taxo_types en plaats deze in de
    # bijbehorende map
    build_hmms(taxo_types, taxonomy_type)

    # Maak de hmm database om vervolgens in te kunnen zoeken
    hmm_db(taxo_types, taxonomy_type)

