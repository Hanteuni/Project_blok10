import json
import traceback
import tqdm


def json_loader(jason_file,hmm_file):
    counter = 0
    temp_ls = []
    output_ls = []
    output_dict = {}
    with open(jason_file,"r") as json_file, open(hmm_file,"r") as hmm_output:
        jason_data = json.load(json_file)
        hmm_output.readline()
        hmm_output.readline()
        for info in jason_data:
            for line in hmm_output:
                hmm_data = line.split("- ")
                if hmm_data[1].strip().__contains__(info):
                    if counter == 3:
                        counter = 0
                        output_ls.append(temp_ls)
                        print(output_ls, score, e_val)
                        output_dict[info] = {"tax 1": output_ls, "score": score, "e-val": e_val}
                        temp_ls = []
                        output_ls = []
                        break
                    e_val, score = hmm_parser(hmm_data[2])
                    temp_ls.append(hmm_data[0].strip())
                    counter += 1





def hmm_parser(hmm_data):
    hmm_data = hmm_data.strip().split(" ")
    e_val = hmm_data[0]
    score = hmm_data[2]
    return e_val, score

def result_to_json(hdrs, e_val, score, annotation):
    pass


if __name__ == '__main__':
    jason_file = "new_json.json"
    hmm_file = "forward_matches.csv.tblout"
    json_loader(jason_file,hmm_file)
