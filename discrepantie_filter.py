import json
import tqdm

import matplotlib.pyplot as plt
from Bio import Entrez

TAXONOMY_LIST = ["p", "c", "o", "f", "g", "sp", "str"]
COUNTER_DICT = {"no mistake": 0, "mistake": 0}


def file_reader(forward_file_name, reverse_file_name, ):
    """Reads the both files at the same time, gets the parsing results and writes away the files
    :param forward_file_name: tsv file which contains the taxonomy of BLAST of the forward reads
    :param reverse_file_name: tsv file which contains the taxonomy of BLAST of the reverse reads
    :return: A written .json file named ALL_BLAST.json
    """
    json_file = {}
    # dictionary for plots
    counter_dict = {"No discrepancy": 0, "Class": 0, "Order": 0, "Family": 0, "Genus": 0, "Species": 0,
                    "forward read empty": 0, "reverse read empty": 0, "both reads empty": 0}
    with open(forward_file_name, "r") as ffile, open(reverse_file_name) as rfile:
        ffile.readline()
        rfile.readline()
        print("Parsing and ordering .tsv content")
        for fline, rline in tqdm.tqdm(zip(ffile, rfile), total=144206, desc="progress"):
            tax_dict_forward = {}
            tax_dict_reverse = {}
            fsplit = fline.split("\t")
            rsplit = rline.split("\t")
            # filling up all empty reads, preventing index errors
            for i in range(42):
                try:
                    fsplit[i]
                except IndexError:
                    fsplit.append("")
                try:
                    rsplit[i]
                except IndexError:
                    rsplit.append("")

            tax_dict_forward[fsplit[0]] = [fsplit[10], fsplit[21], fsplit[32]]
            tax_dict_reverse[rsplit[0]] = [rsplit[10], rsplit[21], rsplit[32]]
            tax_list_forward = [fsplit[10], fsplit[21], fsplit[32]]
            tax_list_reverse = [rsplit[10], rsplit[21], rsplit[32]]
            # checks whether taxonomy is missing and filling them into a list
            full_tax_list_forward = []
            full_tax_list_reverse = []
            for tax_forward in tax_list_forward:
                part_tax_list_forward = fill_empty(tax_list=tax_forward)
                full_tax_list_forward.append(part_tax_list_forward)
            for tax_reverse in tax_list_reverse:
                part_tax_list_reverse = fill_empty(tax_list=tax_reverse)
                full_tax_list_reverse.append(part_tax_list_reverse)
            disc_type = discrepantie_search(tax_dict_forward, tax_dict_reverse)
            counter_dict[disc_type] += 1
            try:
                json_file[fsplit[0]] = {
                    "blast_gelijk": "vul met dispecantie blast",
                    "hmm_gelijk": "vul met type_discrepantie",
                    "forward_sequentie": {
                        "scoring": 0,
                        "e_val": 0,
                        "sequentie": fsplit[2],
                        "taxonomie_blast_domain": {
                            "tax1_domain": {
                                "annotatie": [
                                    "vul_met_taxonomie_niveaus"
                                ]
                            },
                            "tax2_domain": {
                                "annotatie": [
                                    "vul_met_taxonomie_niveaus"
                                ]
                            },
                            "tax3_domain": {
                                "annotatie": [
                                    "vul_met_taxonomie_niveaus"
                                ]
                            }
                        },
                        "taxonomie_blast_kingdom": {
                            "tax1_kingdom": {
                                "annotatie": full_tax_list_forward[0][0]
                            },
                            "tax2_kingdom": {
                                "annotatie": full_tax_list_forward[1][0]
                            },
                            "tax3_kingdom": {
                                "annotatie": full_tax_list_forward[2][0]
                            }
                        },
                        "taxonomie_blast_phylum": {
                            "tax1_phylum": {
                                "annotatie": full_tax_list_forward[0][1]
                            },
                            "tax2_phylum": {
                                "annotatie": full_tax_list_forward[1][1]
                            },
                            "tax3_phylum": {
                                "annotatie": full_tax_list_forward[2][1]
                            }
                        },
                        "taxonomie_blast_class": {
                            "tax1_class": {
                                "annotatie": full_tax_list_forward[0][2]
                            },
                            "tax2_class": {
                                "annotatie": full_tax_list_forward[1][2]
                            },
                            "tax3_class": {
                                "annotatie": full_tax_list_forward[2][2]
                            }
                        },
                        "taxonomie_blast_order": {
                            "tax1_order": {
                                "annotatie": full_tax_list_forward[0][3]
                            },
                            "tax2_order": {
                                "annotatie": full_tax_list_forward[1][3]
                            },
                            "tax3_order": {
                                "annotatie": full_tax_list_forward[2][3]
                            }
                        },
                        "taxonomie_blast_family": {
                            "tax1_family": {
                                "annotatie": full_tax_list_forward[0][4]
                            },
                            "tax2_family": {
                                "annotatie": full_tax_list_forward[1][4]
                            },
                            "tax3_family": {
                                "annotatie": full_tax_list_forward[2][4]
                            }
                        },
                        "taxonomie_blast_genus": {
                            "tax1_genus": {
                                "annotatie": full_tax_list_forward[0][5]
                            },
                            "tax2_genus": {
                                "annotatie": full_tax_list_forward[1][5]
                            },
                            "tax3_genus": {
                                "annotatie": full_tax_list_forward[2][5]
                            }
                        },
                        "taxonomie_blast_species": {
                            "tax1_species": {
                                "annotatie": full_tax_list_forward[0][6]
                            },
                            "tax2_species": {
                                "annotatie": full_tax_list_forward[1][6]
                            },
                            "tax3_species": {
                                "annotatie": full_tax_list_forward[2][6]
                            }
                        }
                    },
                    "reverse_sequentie":
                        {
                            "sequentie": rsplit[2],
                            "scoring": 0,
                            "e_val": 0,
                            "taxonomie_blast_domain": {
                                "tax1_domain": {
                                    "annotatie": [
                                        "vul_met_taxonomie_niveaus"
                                    ]
                                },
                                "tax2_domain": {
                                    "annotatie": [
                                        "vul_met_taxonomie_niveaus"
                                    ]
                                },
                                "tax3_domain": {
                                    "annotatie": [
                                        "vul_met_taxonomie_niveaus"
                                    ]
                                }
                            },
                            "taxonomie_blast_kingdom": {
                                "tax1_kingdom": {
                                    "annotatie": full_tax_list_reverse[0][0]
                                },
                                "tax2_kingdom": {
                                    "annotatie": full_tax_list_reverse[1][0]
                                },
                                "tax3_kingdom": {
                                    "annotatie": full_tax_list_reverse[2][0]
                                }
                            },
                            "taxonomie_blast_phylum": {
                                "tax1_phylum": {
                                    "annotatie": full_tax_list_reverse[0][1]
                                },
                                "tax2_phylum": {
                                    "annotatie": full_tax_list_reverse[1][1]
                                },
                                "tax3_phylum": {
                                    "annotatie": full_tax_list_reverse[2][1]
                                }
                            },
                            "taxonomie_blast_class": {
                                "tax1_class": {
                                    "annotatie": full_tax_list_reverse[0][2]
                                },
                                "tax2_class": {
                                    "annotatie": full_tax_list_reverse[1][2]
                                },
                                "tax3_class": {
                                    "annotatie": full_tax_list_reverse[2][2]
                                }
                            },
                            "taxonomie_blast_order": {
                                "tax1_order": {
                                    "annotatie": full_tax_list_reverse[0][3]
                                },
                                "tax2_order": {
                                    "annotatie": full_tax_list_reverse[1][3]
                                },
                                "tax3_order": {
                                    "annotatie": full_tax_list_reverse[2][3]
                                }
                            },
                            "taxonomie_blast_family": {
                                "tax1_family": {
                                    "annotatie": full_tax_list_reverse[0][4]
                                },
                                "tax2_family": {
                                    "annotatie": full_tax_list_reverse[1][4]
                                },
                                "tax3_family": {
                                    "annotatie": full_tax_list_reverse[2][4]
                                }
                            },
                            "taxonomie_blast_genus": {
                                "tax1_genus": {
                                    "annotatie": full_tax_list_reverse[0][5]
                                },
                                "tax2_genus": {
                                    "annotatie": full_tax_list_reverse[1][5]
                                },
                                "tax3_genus": {
                                    "annotatie": full_tax_list_reverse[2][5]
                                }
                            },
                            "taxonomie_blast_species": {
                                "tax1_species": {
                                    "annotatie": full_tax_list_reverse[0][6]
                                },
                                "tax2_species": {
                                    "annotatie": full_tax_list_reverse[1][6]
                                },
                                "tax3_species": {
                                    "annotatie": full_tax_list_reverse[2][6]
                                }
                            }
                        }
                }
            except IndexError:
                print(full_tax_list_forward)
    print("preparing transfer to json file")
    with open("data/ALL_BLAST.json", "w+") as new_json:
        print("uploading the jason file... ")
        json.dump(json_file, new_json)
        print("file is done")
    return counter_dict


def fill_empty(tax_list):
    """This function fills in the gaps in the BLAST annotation with "".
    Alternatively the annotation can be filled by the taxonomy database although this takes a very long time
    :param tax_list: A list containing the taxonomy of the BLAST output
    :return: A list containing the BLAST annotation where the list is 8 long.
    """
    tax_list_split = tax_list.split("|")
    missing_ls = []
    # checks if there is a taxonomy level missing; also excludes empty annotation
    if 8 > len(tax_list_split) > 1:
        for tax in tax_list_split:
            # organism and taxonomy levels are split from one another
            tax_niveau = tax.split("_")
            if len(tax_niveau) > 1:
                missing_ls.append(tax_niveau[1])
        missing_set = set(missing_ls)
        search_organism = tax_list_split[-2]
        search_organism, _ = search_organism.split("_")
        # looking which taxonomy levels(s) are missing
        missing_tax = set(TAXONOMY_LIST) - missing_set
        for tax in missing_tax:
            index = TAXONOMY_LIST.index(tax)
            # looking in the NCBI taxonomy db for missing tax levels
            # WARNING; this takes a very long time (also you might get kicked out from the NCBI server)
            # filler_organism = tax_get(search_organism, index)
            tax_list_split.insert(index, "")
        COUNTER_DICT["mistake"] += 1
    elif len(tax_list_split) == 1:
        tax_list_split = ["", "", "", "", "", "", "", ""]
    return tax_list_split


def tax_get(search_organism, index):
    """This function searches through the taxonomy database of the NCBI online. WARNING you might get blocked from the
    NCBI server if there are a lot of reads.
    :param search_organism: Organism of which the accession id_ncbi will be retrieved.
    :param index: the index which is used for the taxonomy level
    :return: A full list of organisms retrieved from the NCBI database
    """
    Entrez.email = "probalyjunk@outlook.com"  # Always tell NCBI who you are
    # searches NCBI taxonomy db for the id_ncbi of 2nd to last organism in the tax split list; this is usually species
    id_handle = Entrez.esearch(db="Taxonomy", term=search_organism)
    id_record = Entrez.read(id_handle)
    try:
        # getting the tax id_ncbi for the e-fetch
        id_ncbi = id_record["IdList"][0]
        tax_handle = Entrez.efetch(db="Taxonomy", id=id_ncbi, retmode="xml")
        tax_records = Entrez.read(tax_handle)
        # creating a list of the full taxonomy of the creature
        tax_list = tax_records[0]["Lineage"].split(";")
        # adding +2 on the index since we don't use the first 2 taxonomy levels
        filler_organism = tax_list[index + 2]
        return filler_organism
    except IndexError:
        # if the organism can't be found the NCBI taxonomy it returns ""
        return ""


def discrepantie_search(tax_dict_forward, tax_dict_reverse):
    """Looks at which taxonomy level the discrepancy appears. It also checks whether one or both of the reads
    annotations is empty. This functions classifies the discrepancies into the following levels:
    "Class", "Order", "Family", "Genus", "Species" & "No discrepancy". If no discrepancies are found the function
    classifies it no discrepancy.
    :param tax_dict_forward: A dictionary contaning the taxonomic information of the forward read
    :param tax_dict_reverse:A dictionary contaning the taxonomic information of the reverse read
    :return: A dictionary containing on which taxonomic level the BLAST differs from one another
    """
    hdrs = ["Class", "Order", "Family", "Genus", "Species", "No discrepancy"]
    disc_type = ""
    for key in tax_dict_forward:
        # checks whether both reads are empty
        if tax_dict_forward.get(key)[0] == "\n" and tax_dict_reverse.get(key)[0] == "\n":
            disc_type = "both reads empty"
        if tax_dict_forward.get(key)[0] != tax_dict_reverse.get(key)[0]:
            # checks whether the forward read is empty
            if tax_dict_forward.get(key)[0] == "\n":
                disc_type = "forward read empty"
            # checks whether the reverse read is empty
            elif tax_dict_reverse.get(key)[0] == "\n":
                disc_type = "reverse read empty"
                # Only looks at the 1st top hit
            elif tax_dict_forward.get(key)[0] != tax_dict_reverse.get(key)[0]:
                disc_type = tax_difference(tax_dict_forward, tax_dict_reverse, key, hdrs)
        elif tax_dict_forward.get(key)[0] == tax_dict_reverse.get(key)[0]:
            disc_type = "No discrepancy"
    return disc_type


def tax_difference(tax_dict_forward, tax_dict_reverse, key, hdrs):
    """This function searches the difference in between the two dictionaries. And returns the highest taxonomic level on
    which a discrepancy occurs.
    :param tax_dict_forward: This dictionary contains the taxonomic information of the forward reads
    :param tax_dict_reverse:This dictionary contains the taxonomic information of the reverse reads
    :param key: The read header of which taxonomic information will be compared
    :param hdrs: a list with the taxonomic levels.
    :return: The highest taxonomic level at which the discrepancy was found.
    """
    temp_l1 = tax_dict_forward.get(key)[0].split("|")
    temp_l2 = tax_dict_reverse.get(key)[0].split("|")
    tax_set1 = set(temp_l1[1:6])
    tax_set2 = set(temp_l2[1:6])
    # checks the difference in the taxonomy
    difference = tax_set1 - tax_set2
    index = 5 - len(difference)
    return hdrs[index]


def discrepancy_plot(data_dict):
    """This function makes a plot that visualises the distribution between the discrepancies.
    :param data_dict: A dictionary containing counts of the different discrepancies
    :return: A plot visualising the difference in the discrepancies
    """
    plt.bar(range(len(data_dict)), list(data_dict.values()), align='center')
    plt.xticks(range(len(data_dict)), list(data_dict.keys()), rotation=45)
    plt.title("BLAST discrepanties distributie tussen forward en reverse reads")
    plt.ylabel("Aantal discrepanties")
    plt.xlabel("Discrepantie type")
    plt.tight_layout()
    plt.show()


def counter_for_analysis(counter_analysis):
    """Counts the different discrepancies so they can be visualised into a plot or be printed out. This can be used to
    show the distrubution of the discrepancies. Or count how much of the data contains a discrepancy.
    :param counter_analysis: A counter containing the taxonomic level
    :return: a print statement on the % in discrepancy
    """
    total = 0
    total_class = int(counter_analysis['No discrepancy']) + int(counter_analysis['Class']) + \
                  int(counter_analysis['forward read empty']) + int(
        counter_analysis['reverse read empty']) + int(counter_analysis['both reads empty'])
    total_count = list(counter_analysis.values())
    for number in total_count:
        total += number
    print(f"The percentage discrepancy in class level: ", round(total_class / total * 100, 2), "%")


if __name__ == '__main__':
    ffname = "1_R1_outputfile.tsv"
    rfname = "1_R2_outputfile.tsv"
    counter = file_reader(ffname, rfname)
    discrepancy_plot(counter)
    counter_for_analysis(counter)
