import json


def file_reader(fname, sequentie):
    tax_dict = {}
    old_json_file = open("jason.json", "r+")
    old_json_file.readline(0).strip()
    print(old_json_file.readline(0))
    json_file = json.load(old_json_file)
    old_json_file.truncate(0)
    with open(fname, "r") as file:
        file.readline()
        for line in file:
            try:
                temp_ls = line.split("\t")
                if sequentie == "forward":
                    json_file[temp_ls[0]] = {'forward_sequentie': {'sequentie': temp_ls[2], 'taxonomie_blast': {
                        'tax1': {'annotatie': temp_ls[10], 'e-value': temp_ls[19], 'scoring': temp_ls[20]},
                        'tax2': {'annotatie': temp_ls[21], 'e-value': temp_ls[30], 'scoring': temp_ls[31]}}},
                                         'reverse_sequentie': {'sequentie': '', 'taxonomie_blast': {
                                             'tax1': {'annotatie': ['vul_met_taxonomie_niveaus'], 'e-value': 0,
                                                      'scoring': 0},
                                             'tax2': {'annotatie': ['vul_met_taxonomie_niveaus'], 'e-value': 0,
                                                      'scoring': 0}}, 'taxonomie_hmms': {
                                             'tax1': {'annotatie': ['vul_met_taxonomie_niveaus'], 'scoring': 0},
                                             'tax2': {'annotatie': ['vul_met_taxonomie_niveaus'],
                                                      'scoring': 0}}}, 'blast_gelijk': 'type_discrepantie',
                                         'hmm_gelijk': 'type_discrepantie'}

                    if sequentie == "reverse":
                        json_file[temp_ls[0]] = {'forward_sequentie': {'sequentie': '', 'taxonomie_blast': {
                            'tax1': {'annotatie': ['vul_met_taxonomie_niveaus'], 'e-value': 0, 'scoring': 0},
                            'tax2': {'annotatie': ['vul_met_taxonomie_niveaus'], 'e-value': 0, 'scoring': 0}},
                                                                   'taxonomie_hmms': {
                                                                       'tax1': {
                                                                           'annotatie': ['vul_met_taxonomie_niveaus'],
                                                                           'scoring': 0},
                                                                       'tax2': {
                                                                           'annotatie': ['vul_met_taxonomie_niveaus'],
                                                                           'scoring': 0}}},
                                             'blast_gelijk': 'type_discrepantie',
                                             'hmm_gelijk': 'type_discrepantie'}
                header = temp_ls[0]
                tax_dict[header] = [temp_ls[10], temp_ls[21], temp_ls[32]]

                #     print("Header: ", temp_ls[0])
                #     print("sequentie: ",temp_ls[2])
                #     print("tax_e-value 1:",temp_ls[19])
                #     print("tax_bit_score 1:",temp_ls[20])
                #     print("tax_e-value 2:",temp_ls[30])
                #     print("tax_bit_score 1:",temp_ls[31])
                #     print("tax_e-value 2:",temp_ls[41])
                #     print("tax_bit_score 1:",temp_ls[42])
                #     print("tax1:",temp_ls[10])
                #     print("tax2:",temp_ls[21])
                #     print("tax3:",temp_ls[32])


            except IndexError:
                if len(temp_ls) >= 10:
                    tax_dict[header] = ""
                elif len(temp_ls) >= 21:
                    tax_dict[header] = temp_ls[10]
                else:
                    tax_dict[header] = temp_ls[10], temp_ls[21]
    json.dump(json_file, old_json_file)
    old_json_file.close()
    return tax_dict


def discrepantie_search():
    fname = "1_R1_outputfile.tsv"
    fname2 = "1_R2_outputfile.tsv"
    tax_dict1 = file_reader(fname, sequentie="forward")
    tax_dict2 = file_reader(fname2, sequentie="reverse")
    hdrs = ["Domain", "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    disc_dict = {}
    # for key in tax_dict1:
    #     if tax_dict1.get(key) == "" and tax_dict2.get(key) == "":
    #         disc_dict[key] = "both reads empty"
    #     if tax_dict1.get(key) != tax_dict2.get(key):
    #         if tax_dict1.get(key) == "":
    #             disc_dict[key] = "forward read empty"
    #         elif tax_dict2.get(key) == "":
    #             disc_dict[key] = "reverse read empty"
    #             # hij kijkt alleen naar de eerste hit en niet naar de 2e en 3e
    #         elif tax_dict1.get(key)[0] != tax_dict2.get(key)[0]:
    #             tax_splitter(tax_dict1,tax_dict2,disc_dict,key,hdrs)

    # counter = {} # yo pik we hebben jullie werk gedaan ook al was het voor bugfixing +1 voor chrissie
    # for key in disc_dict:
    #     if disc_dict.get(key) in counter:
    #         counter[disc_dict.get(key)] += 1
    #     else:
    #         counter[disc_dict.get(key)] = 1


def tax_splitter(tax_dict1, tax_dict2, disc_dict, key, hdrs):
    tax_set1 = set(tax_dict1.get(key)[0].split("|"))
    tax_set2 = set(tax_dict2.get(key)[0].split("|"))
    difference = tax_set1 - tax_set2
    # print(difference)
    # print(len(difference))
    # print(hdrs[len(difference)])
    disc_dict[key] = "difference on " + hdrs[len(difference) - 1]


if __name__ == '__main__':
    discrepantie_search()
