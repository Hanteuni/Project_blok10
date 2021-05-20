import json
import traceback
import tqdm

def json_loader(jason_file, hmm_file):
    counter = 0
    temp_ls = []
    output_ls = []
    output_dict = {}
    result_dict = {}
    with open(jason_file, "r") as json_file, open(hmm_file, "r") as hmm_output:
        jason_data = json.load(json_file)
        hmm_output.readline()
        hmm_output.readline()
        for info in tqdm.tqdm(jason_data, total=len(jason_file), desc="progress"):

            for line in hmm_output:
                if not line.startswith("#"):
                    hmm_data = line.split("- ")
                    if hmm_data[1].strip().__contains__(info):
                        if counter == 3:
                            counter = 0
                            result_dict[info] = temp_ls
                            temp_ls = []
                            break
                        if counter <3:
                            e_val, score = hmm_parser(hmm_data[2])
                            temp_ls.extend([hmm_data[0].strip(), e_val, score])
                            counter += 1

            # counter = 0
            # print(info, temp_ls)
            # result_dict[info] = temp_ls
            # temp_ls = []

    return result_dict

def json_loader_steffen2(jason_file, hmm_file):
    counter = 0
    temp_top = []
    temp_ls = []
    result_dict = {}
    latest_header = ""
    with open(hmm_file, "r") as hmm_output:
        for line in hmm_output:
            if not line.startswith("#"):
                hmm_data = line.split("- ")
                header = hmm_data[1].strip().split("|")[0]
                # print(temp_top)
                if temp_top:
                    if header != latest_header:
                        # print(header, latest_header)
                        # print(temp_top[:3])
                        if len(temp_top) <3:
                           loops = 3 - len(temp_top)
                           for i in range(loops):
                               temp_top.append([["emppty"], [""], [""]])
                        result_dict[header] = temp_top[:3]
                        temp_top = []
                        latest_header = header
                        e_val, score = hmm_parser(hmm_data[2])
                        temp_top.append([hmm_data[0].strip(), e_val, score])
                    else:
                        e_val, score = hmm_parser(hmm_data[2])
                        temp_top.append([hmm_data[0].strip(), e_val, score])
                        # print("else")

                else:
                    e_val, score = hmm_parser(hmm_data[2])
                    temp_top = [[hmm_data[0].strip(), e_val, score]]
                    latest_header = header
                    # print("else")
    return result_dict





def json_loader_steffen(jason_file, hmm_file):
    counter = 0
    temp_ls = []
    output_ls = []
    output_dict = {}
    result_dict = {}
    with open(jason_file, "r") as json_file, open(hmm_file, "r") as hmm_output:
        jason_data = json.load(json_file)
        hmm_output.readline()
        hmm_output.readline()
        lines = 0
        contain = 0
        loop = 0
        keys_in_hmms = 0
        for info in tqdm.tqdm(jason_data, total=len(jason_file), desc="progress"):
            # print(info)
            lines = lines +1
            loop = 0
            for line in hmm_output:
                loop = loop +1

                if not line.startswith("#"):
                    hmm_data = line.split("- ")
                    if hmm_data[1].strip().__contains__(info):
                        contain = contain + 1

                        if counter == 3:
                            keys_in_hmms += 1
                            counter = 0
                            result_dict[info] = temp_ls
                            temp_ls = []
                            # why is there a break here ???
                            print("writing ")
                            break
                        if counter <= 3:
                            e_val, score = hmm_parser(hmm_data[2])
                            temp_ls.extend([hmm_data[0].strip(), e_val, score])
                            counter += 1

                    # else:
                        # print(hmm_data, "------",  info)
                if loop == 8725760:
                    print(info)


            # result_dict[info] = temp_ls
            # temp_ls = []
            # print(loop)
    # print("lines: ", lines)
    # print("keys: ", keys_in_hmms)
    # print("contains: ", contain)
    # print("loop: ", loop)
    return result_dict




def hmm_discrepancies(result_forward_dict, result_reverse_dict):
    json_file = {}
    counter_total = 0
    counter_discrepancy = 0

    for info in result_reverse_dict:
        forward_names = result_forward_dict.get(info)
        reverse_names = result_reverse_dict.get(info)
        print(reverse_names)
        print(forward_names)
        print(info)
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


def Chlamydiia_gives_us_problems():
    with open("reverse_teamviewer.csv", "r") as f:
        lines = f.readlines()
    with open("reverse_teamviewer.csv", "w") as f:
        for line in lines:
            if line.strip(
                    "\n") != "Chlamydiia           -          M04481:146:000000000-C84RG:1:1101:9404:6731|reverse -                3.7   -2.4   0.4       6.7   -3.3   0.4   1.1   1   0   0   1   1   1   0 -":
                f.write(line)


def hmm_discrepancies_top3(result_forward_dict, result_reverse_dict):
    count = 0
    count2 = 0

    for info in result_forward_dict:
        forward_set = set()
        reverse_set = set()
        forward_names = result_forward_dict.get(info)
        reverse_names = result_reverse_dict.get(info)
        if forward_names is not None:
            forward_list = [forward_names[0], forward_names[3], forward_names[6]]
            forward_set = set(forward_list)
        if reverse_names is not None:
            reverse_list = [reverse_names[0], reverse_names[3], reverse_names[6]]
            reverse_set = set(reverse_list)
        difference = forward_set - reverse_set
        # print(difference)
        # [hit 1,hit 2, hit 3] [hit 4, hit 5, hit 6]
        if len(difference) <= 3:
            count += 1
        else:
            count2 += 1
    print(count, count2)


def hmm_parser(hmm_data):
    hmm_data = hmm_data.strip().split(" ")
    e_val = hmm_data[0]
    score = hmm_data[2]
    return e_val, score


def save_result_json(result_forward_dict, result_reverse_dict, info, result="", json_file={}):
    # print(result_reverse_dict[info])
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
                "tax1_phylum": {
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
    with open("All_HMM.json", "w+") as new_json:
        print("uploading the jason file... ")
        json.dump(json_file, new_json)
        print("file is done")

if __name__ == '__main__':
    jason_file = "DOOM.json"
    hmm_file_forward = "forward_matches.csv.tblout"
    hmm_file_reverse = "reverse_teamviewer.csv"
    print("starting forward")
    result_forward_dict = json_loader_steffen2(jason_file, hmm_file=hmm_file_forward)
    print("starting reverse")
    result_reverse_dict = json_loader_steffen2(jason_file, hmm_file=hmm_file_reverse)
    forward_file = open("forward_dict", "w+")
    json.dump(result_forward_dict, forward_file)
    reverse_file = open("reverse_dict", "w+")
    json.dump(result_forward_dict, reverse_file)
    print("forawrd", len(result_forward_dict))
    print("reverse: ", len(result_reverse_dict))

    json_file, counter_discrepancy, counter_total = hmm_discrepancies(result_forward_dict, result_reverse_dict)

    print(f"The percentage discrepancy in class level: ", round(counter_discrepancy / counter_total * 100,2), "%")
    write_to_json(json_file)
    # Chlamydiia_gives_us_problems()