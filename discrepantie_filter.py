import json, tqdm
import matplotlib.pyplot as plt
import math


def file_reader(ffname, rfname, ):
    json_file = {}
    counter = {"No discrepancy": 0, "Class": 0, "Order": 0, "Family": 0, "Genus": 0, "Species": 0,
               "forward read empty": 0, "reverse read empty": 0, "both reads empty": 0}
    with open(ffname, "r") as ffile, open(rfname) as rfile:
        ffile.readline()
        rfile.readline()
        print("Parsing and ordering .tsv content")
        for fline, rline in tqdm.tqdm(zip(ffile, rfile), total=150000, desc="progress"):
            tax_dict1 = {}
            tax_dict2 = {}
            fsplit = fline.split("\t")
            # print(fsplit)
            rsplit = rline.split("\t")
            # print(rsplit)

            for i in range(33):
                try:
                    fsplit[i]
                except IndexError:
                    fsplit.append("")
                try:
                    rsplit[i]
                except IndexError:
                    rsplit.append("")

            tax_dict1[fsplit[0]] = [fsplit[10], fsplit[21], fsplit[32]]
            tax_dict2[rsplit[0]] = [rsplit[10], rsplit[21], rsplit[32]]

            disc_type = discrepantie_search(tax_dict1, tax_dict2)
            counter[disc_type] += 1
            json_file[fsplit[0]] = {'forward_sequentie': {'sequentie': fsplit[2], 'taxonomie_blast': {'tax1':
                                                                                                          {'annotatie':
                                                                                                               fsplit[
                                                                                                                   10],
                                                                                                           'e-value':
                                                                                                               fsplit[
                                                                                                                   19],
                                                                                                           'scoring':
                                                                                                               fsplit[
                                                                                                                   20]},
                                                                                                      'tax2': {
                                                                                                          'annotatie':
                                                                                                              fsplit[
                                                                                                                  21],
                                                                                                          'e-value':
                                                                                                              fsplit[
                                                                                                                  30],
                                                                                                          'scoring':
                                                                                                              fsplit[
                                                                                                                  31]}}},
                                    'reverse_sequentie': {'sequentie': rsplit[2], 'taxonomie_blast':
                                        {'tax1': {'annotatie': rsplit[10], 'e-value': rsplit[19],
                                                  'scoring': rsplit[20]},
                                         'tax2': {'annotatie': rsplit[21], 'e-value': rsplit[30],
                                                  'scoring': rsplit[31]}}},
                                    'blast_gelijk': disc_type,
                                    'hmm_gelijk': 'type_discrepantie'}
        print("preparing transfer to json file")
        with open("DOOM.json", "w+") as new_json:
            print("uploading the jason file... ")
            json.dump(json_file, new_json)
            print("file is done")
        return counter


def discrepantie_search(tax_dict1, tax_dict2):
    hdrs = ["Class", "Order", "Family", "Genus", "Species", "No discrepancy"]
    disc_type = ""
    for key in tax_dict1:
        if tax_dict1.get(key)[0] == "\n" and tax_dict2.get(key)[0] == "\n":
            disc_type = "both reads empty"
        if tax_dict1.get(key)[0] != tax_dict2.get(key)[0]:
            if tax_dict1.get(key)[0] == "\n":
                disc_type = "forward read empty"
            elif tax_dict2.get(key)[0] == "\n":
                disc_type = "reverse read empty"
                # hij kijkt alleen naar de eerste hit en niet naar de 2e en 3e
            elif tax_dict1.get(key)[0] != tax_dict2.get(key)[0]:
                disc_type = tax_splitter(tax_dict1, tax_dict2, key, hdrs)
        elif tax_dict1.get(key)[0] == tax_dict2.get(key)[0]:
            disc_type = "No discrepancy"
    return disc_type
    # counter = {} # yo pik we hebben jullie werk gedaan ook al was het voor bugfixing +1 voor chrissie
    # for key in disc_dict:
    #     if disc_dict.get(key) in counter:
    #         counter[disc_dict.get(key)] += 1
    #     else:
    #         counter[disc_dict.get(key)] = 1


def tax_splitter(tax_dict1, tax_dict2, key, hdrs):
    temp_l1 = tax_dict1.get(key)[0].split("|")
    temp_l2 = tax_dict2.get(key)[0].split("|")
    tax_set1 = set(temp_l1[1:6])
    tax_set2 = set(temp_l2[1:6])
    difference = tax_set1 - tax_set2
    # print(difference)
    index = 5 - len(difference)
    return hdrs[index]


def empty_json():
    old_json_file = open("DOOM.json", "r+")
    # old = json.load(old_json_file)

    old_json_file.truncate(0)
    new_json_file = open("back_up.json", "r+")
    new = json.load(new_json_file)
    json.dump(new, old_json_file)
    old_json_file.close()


def discrepancy_plot(data_dict):
    plt.bar(range(len(data_dict)), list(data_dict.values()), align='center')
    plt.xticks(range(len(data_dict)), list(data_dict.keys()), rotation=45)
    plt.title("BLAST discrepancy distribution between forward and reverse reads")
    plt.ylabel("Discrepancies count")
    plt.xlabel("Discrepancy type")
    plt.tight_layout()
    plt.show()


def counter_for_analysis(counter):
    total = 0
    total_class = int(counter['No discrepancy']) + int(counter['Class']) + int(counter['forward read empty']) + int(
        counter['reverse read empty']) + int(counter['both reads empty'])
    total_count = list(counter.values())
    for number in total_count:
        total += number
    print(f"The percentage discrepancy in class level: ", round(total_class / total * 100,2), "%")


if __name__ == '__main__':
    # empty_json()
    ffname = "1_R1_outputfile.tsv"
    rfname = "1_R2_outputfile.tsv"
    counter = file_reader(ffname, rfname)
    # discrepancy_plot(counter)
    counter_for_analysis(counter)
