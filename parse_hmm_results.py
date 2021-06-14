import json


def hmm_output_splitter(hmm_file):
    """This function reads in the hmm output file (.tblout) and parses the data within it.
    It takes the top 3 hits of the hmm_file(the annotation with the highest score). If there are no top 3 hits it will
    fill the result with "empty". This function also calls on the hmm_parser function.
    :param hmm_file: A file with the output of the hmmer tool in a .tblout
    :return: A dictionary with the top 3 hits of the the hmmer tool output with the read data headers as keys.
    """
    temp_top = []
    result_dict = {}
    latest_header = ""
    with open(hmm_file, "r") as hmm_output:
        for line in hmm_output:
            if not line.startswith("#"):
                # Parsing the data from the lines.
                hmm_data = line.split("- ")
                header = hmm_data[1].strip().split("|")[0]
                if temp_top:
                    if header != latest_header:
                        # Only picks the top 3 and resets if there aren't 3 results
                        if len(temp_top) < 3:
                            loops = 3 - len(temp_top)
                            for i in range(loops):
                                temp_top.append("emppty")
                        result_dict[header] = temp_top[:3]
                        temp_top = []
                        latest_header = header
                        e_val, score = hmm_parser(hmm_data[2])
                        temp_top.append([hmm_data[0].strip(), e_val, score])
                    else:
                        e_val, score = hmm_parser(hmm_data[2])
                        temp_top.append([hmm_data[0].strip(), e_val, score])
                else:
                    e_val, score = hmm_parser(hmm_data[2])
                    temp_top = [[hmm_data[0].strip(), e_val, score]]
                    latest_header = header
    return result_dict


def hmm_discrepancies(result_forward_dict, result_reverse_dict):
    """This functions checks the output the hmmer output files of the forward and reverse reads and then compares both
    of their content and checks if the compare well to one another. This function also call on the save_result_to_json
    function.
    :param result_forward_dict: A dictionary with the top 3 hits of the the hmmer tool output with
    the forward read data headers as keys
    :param result_reverse_dict: A dictionary with the top 3 hits of the the hmmer tool output with the
     reverse read data headers as keys
    :return:
    json_file: A dictionary containing the top3 hits, the discrepancy between the reads and the headers as key
    Counter_discrepancy: A dictionair for analysis containing the counts of discrepancies
    counter_total: An int containing the total amount of comparisons
    """
    json_file = {}
    counter_total = 0
    counter_discrepancy = 0
    # only check the reverse dict for headers;
    for info in result_reverse_dict:
        forward_names = result_forward_dict.get(info)
        reverse_names = result_reverse_dict.get(info)
        # checks whether or not the forward or reverse result is empty.
        if reverse_names[0] is not None and forward_names[0] is not None:
            if forward_names[0] == reverse_names[0]:
                counter_total += 1
                json_file = save_result_json(result_forward_dict, result_reverse_dict, info, result="No Discrepancy",
                                             json_file=json_file)
            else:
                counter_total += 1
                counter_discrepancy += 1
                json_file = save_result_json(result_forward_dict, result_reverse_dict, info, result="Discrepancy",
                                             json_file=json_file)
    return json_file, counter_discrepancy, counter_total


def hmm_parser(hmm_data):
    """This function retrieves e-value & score of the hmm output.
    :param hmm_data: data containing the e-value and score of the hmm result
    :return: e-value and score of the hmm result
    """
    hmm_data = hmm_data.strip().split(" ")
    e_val = hmm_data[0]
    score = hmm_data[2]
    return e_val, score


def save_result_json(result_forward_dict, result_reverse_dict, info, result="", json_file={}):
    """Writes all of the hmm information to a .json formatted dictionary.
    :param result_forward_dict: A dictionary with the top 3 hits of the the hmmer tool output with the
    forward read data headers as keys.
    :param result_reverse_dict:  A dictionary with the top 3 hits of the the hmmer tool output with the
    reverse read data headers as keys.
    :param info: the header of the read data
    :param result: whether there was a discrepancy between the hmm's
    :param json_file: a dictionary that contains the information for the .json
    :return: a .json formatted dictionary
    """
    json_file[info] = {
        "forward_sequentie": {
            "sequentie": "",
            "taxonomie_hmms_domain": {
                "tax1_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_kingdom": {
                "tax1_kingdom": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_kingdom": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_phylum": {
                "tax1_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_class": {
                "tax1_class": {
                    "annotatie": result_forward_dict[info][0][0],
                    "scoring": result_forward_dict[info][0][1],
                    "e_val": result_forward_dict[info][0][2]
                },
                "tax2_class": {
                    "annotatie": result_forward_dict[info][1][0],
                    "scoring": result_forward_dict[info][1][1],
                    "e_val": result_forward_dict[info][1][2]
                },
                "tax3_class": {
                    "annotatie": result_forward_dict[info][2][0],
                    "scoring": result_forward_dict[info][2][1],
                    "e_val": result_forward_dict[info][2][2]
                },
                "discrepancy": result
            },
            "taxonomie_hmms_order": {
                "tax1_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_family": {
                "tax1_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_genus": {
                "tax1_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_species": {
                "tax1_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            }
        },
        "reverse_sequentie": {
            "sequentie": "",
            "taxonomie_hmms_domain": {
                "tax1_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_kingdom": {
                "tax1_kingdom": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_kingdom": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_domain": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_phylum": {
                "tax1_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_phylum": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_class": {
                "tax1_class": {
                    "annotatie": result_reverse_dict[info][0][0],
                    "scoring": result_reverse_dict[info][0][1],
                    "e_val": result_reverse_dict[info][0][2]
                },
                "tax2_class": {
                    "annotatie": result_reverse_dict[info][1][0],
                    "scoring": result_reverse_dict[info][1][1],
                    "e_val": result_reverse_dict[info][1][2]
                },
                "tax3_class": {
                    "annotatie": result_reverse_dict[info][2][0],
                    "scoring": result_reverse_dict[info][2][1],
                    "e_val": result_reverse_dict[info][2][2]
                },
                "discrepancy": result
            },
            "taxonomie_hmms_order": {
                "tax1_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_order": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_family": {
                "tax1_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_family": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_genus": {
                "tax1_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_genus": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            },
            "taxonomie_hmms_species": {
                "tax1_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax2_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                },
                "tax3_species": {
                    "annotatie": [
                        "vul_met_taxonomie_niveaus"
                    ],
                    "scoring": 0,
                    "e_val": 0
                }
            }
        }}
    return json_file


def write_to_json(json_file):
    """ Writes the a dictionary to a .json file
    :param json_file: dictionary that contains information for a .json file
    :return: a .json file containing the following information of the .json; header of the hmm, top3 results, score,
    e-value and whether it has a discrepancy or not.
    """
    with open("All_HMM.json", "w+") as new_json:
        print("uploading the jason file... ")
        json.dump(json_file, new_json)
        print("file is done")


if __name__ == '__main__':
    jason_file = "ALL_BLAST.json"
    hmm_file_forward = "forward_matches.csv.tblout"
    hmm_file_reverse = "reverse_teamviewer.csv"
    print("starting forward")
    result_forward_dict = hmm_output_splitter(hmm_file=hmm_file_forward)
    print("starting reverse")
    result_reverse_dict = hmm_output_splitter(hmm_file=hmm_file_reverse)
    forward_file = open("forward_dict", "w+")
    json.dump(result_forward_dict, forward_file)
    reverse_file = open("reverse_dict", "w+")
    json.dump(result_forward_dict, reverse_file)
    json_file, counter_discrepancy, counter_total = hmm_discrepancies(result_forward_dict, result_reverse_dict)
    print(f"The percentage discrepancy in class level: ", round(counter_discrepancy / counter_total * 100, 2), "%")
    write_to_json(json_file)
