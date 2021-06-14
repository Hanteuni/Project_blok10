"""Dit script zet de hmm output om naar

Author: Teuntje Peeters
Date: Date: 23/11/20"""

import os
import subprocess


def parse_hmmscan(hmmoutput):
    """Maak csv van hmm output

    :param hmmoutput: str - naam input bestand
    :return: hmmscan_output - dictio -
    {accessiecode: [hmm_hit, score, eval, bias]}
    """
    hmmscan_output = {}
    with open(hmmoutput) as inFile:
        for line in inFile:
            if not line.startswith("#"):
                line = line.strip().split()
                query = line[2]
                if query in hmmscan_output:
                    hmmscan_output[query].append(\
                        [line[0], line[5], line[4], line[6]])
                else:
                    hmmscan_output[query] = [[line[0], line[5], line[4], line[6]]]
    return hmmscan_output


def get_unique_hmmscores(values):
    """Haal de unieke hmm uit de values van de dictionary om deze
    lijst te gebruiken bij het converten naar een csv
    :param value: value uit de dictionary
    :return: lijst met unieke hmm
    """
    uniek = []
    for el in values:
        for e in el:
            if e[0] not in uniek:
                uniek.append(e[0])
    return uniek


def convert_to_csv(hmmscan_output, option_nr, option, unique_fn):
    """Convert hmmscan output to csv

    :param hmmscan_output: {accessiecode: [hmm_hit, score, eval, bias]}
    :param option: what value to write? (score, eval or bias) this is an
    integer and the number will be used as index
    :return:
    """
    csv_output = []
    hmm_hits = get_unique_hmmscores(hmmscan_output.values())
    hmm_hits.sort()
    for key, value in hmmscan_output.items():
        temp = ["None"] * len(hmm_hits)
        for v in value:
            index = hmm_hits.index(v[0])
            temp[index] = v[option_nr + 1]
        temp.insert(0, key)
        csv_output.append(temp)
    write_csv(hmm_hits, csv_output, option, unique_fn)


def write_csv(hmm_hits, csv_output, option, unique_fn):
    """Schrijf de daadwerkelijke csv weg

    :param hmm_hits: unieke hmm hits
    :param csv_output: datastructuur met daarin de csv output om het
    gemakkelijk weg te schrijven
    :param option: naam van de type scores dat wordt weggeschreven

    :return:
    """
    #data moet dus andersom..
    filename = "hmmoutput_overview_{}_{}.csv".format(unique_fn, option)
    with open(filename, "w") as inFile:
        inFile.write("\t{}\n".format("\t".join(hmm_hits)))
        for el in csv_output:
            inFile.write("{}\n".format("\t".join(el)))


def convert_to_csv_transposed(hmmscan_output, option_nr, option, unique_fn):
    """Convert hmmscan output to csv

    :param hmmscan_output: {accessiecode: [hmm_hit, score, eval, bias]}
    :param option: what value to write? (score, eval or bias) this is an
    integer and the number will be used as index
    :return:
    """
    csv_output = []
    hmm_hits = get_unique_hmmscores(hmmscan_output.values())
    hmm_hits.sort()
    headers = hmmscan_output.keys()
    for hmm in hmm_hits:
        temp = [hmm]
        for key, value in hmmscan_output.items():
            for v in value:
                if hmm == v[0]:
                    temp.append(v[option_nr+1])
            # temp.insert(0, hmm)
        csv_output.append(temp)
    write_csv_transposed(headers, csv_output, option, unique_fn)


def write_csv_transposed(headers, csv_output, option, unique_fn):
    """Schrijf de daadwerkelijke csv weg

    :param hmm_hits: unieke hmm hits
    :param csv_output: datastructuur met daarin de csv output om het
    gemakkelijk weg te schrijven
    :param option: naam van de type scores dat wordt weggeschreven

    :return:
    """
    filename = "hmmoutput_overview_{}_{}_transposed.csv".format(option, unique_fn)
    with open(filename, "w") as inFile:
        inFile.write("\t{}\n".format("\t".join(headers)))
        for el in csv_output:
            inFile.write("{}\n".format("\t".join(el)))


def move_output_to_directory(taxonomy_type):
    """Verplaats bestanden naar de juiste directory

    :return:
    """
    if not os.path.isdir("hmm_db/{}/hmm_scan_searches/csvoutput".format(
        taxonomy_type)):
        cmd = "mkdir hmm_db/{}/hmm_scan_searches/csvoutput".format(
            taxonomy_type)
        e = subprocess.check_call(cmd, shell=True)

    directory_files = os.listdir()
    for file in directory_files:
        if ".csv" in file and "overview" in file:
            cmd = "mv {} hmm_db/{}/hmm_scan_searches/csvoutput".format(
                file, taxonomy_type)
            e = subprocess.check_call(cmd, shell=True)


if __name__ == '__main__':
    taxonomy_type = "class"
    # Geef de hmm output file die je wilt converteren naar csv
    hmmoutput = "hmm_db/{}/hmm_scan_searches/janne.csv.tblout".\
        format(taxonomy_type)

    unique_filename = "janne"

    # Parse de hmm scan output
    hmmscan_output = parse_hmmscan(hmmoutput)

    # Geef de verschillende opties die je graag uit wilt spugen
    # in de folder
    options = ["score", "eval", "bias"]
    for i in range(len(options)):
        convert_to_csv(hmmscan_output, i, options[i], unique_filename)
        convert_to_csv_transposed(hmmscan_output, i, options[i],
                                  unique_filename)

    # Verplaats de output naar de juiste directory
    move_output_to_directory(taxonomy_type)
