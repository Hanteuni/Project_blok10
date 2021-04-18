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
                        e_val, score = hmm_parser(hmm_data[2])
                        temp_ls.extend([hmm_data[0].strip(), e_val, score])
                        counter += 1
    return result_dict


def hmm_discrepancies(result_forward_dict, result_reverse_dict):
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
        print(difference)
        # [hit 1,hit 2, hit 3] [hit 4, hit 5, hit 6]
        if len(difference) <= 4:
            count += 1
        else:
            count2 += 1
    print(count, count2)


def hmm_parser(hmm_data):
    hmm_data = hmm_data.strip().split(" ")
    e_val = hmm_data[0]
    score = hmm_data[2]
    return e_val, score


def result_to_json(hdrs, e_val, score, annotation):
    pass


if __name__ == '__main__':
    jason_file = "DOOM.json"
    hmm_file_forward = "forward_matches.csv.tblout"
    hmm_file_reverse = "reverse_teamviewer.csv"
    print("starting forward")
    result_forward_dict = json_loader(jason_file, hmm_file=hmm_file_forward)
    print("starting reverse")
    result_reverse_dict = json_loader(jason_file, hmm_file=hmm_file_reverse)
    hmm_discrepancies(result_forward_dict, result_reverse_dict)
