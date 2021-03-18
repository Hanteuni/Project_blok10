import json


def file_reader(ffname, rfname,):
    json_file = {}

    with open(ffname, "r") as ffile, open(rfname) as rfile:
        ffile.readline()
        rfile.readline()

        counter = 0
        for fline, rline in zip(ffile, rfile):
            counter = counter + 1

            fsplit = fline.split("\t")
            # print(fsplit)
            rsplit = rline.split("\t")
            # print(rsplit)

            for i in range(32):
                try:
                    fsplit[i]
                except (IndexError, ValueError):
                    fsplit.append("none")
                try:
                    rsplit[i]
                except (IndexError, ValueError):
                    rsplit.append("none")


            json_file[fsplit[0]] = {'forward_sequentie':
                                            {'sequentie': fsplit[2], 'taxonomie_blast': {'tax1':
                                                    {'annotatie': fsplit[10], 'e-value': fsplit[19],
                                                    'scoring': fsplit[20]}, 'tax2': {'annotatie': fsplit[21],
                                                    'e-value': fsplit[30], 'scoring': fsplit[31]}}},
                                 'reverse_sequentie': {'sequentie': rsplit[2], 'taxonomie_blast': {'tax1':
                                                    {'annotatie': rsplit[10], 'e-value': rsplit[19],
                                                    'scoring': rsplit[20]}, 'tax2': {'annotatie': rsplit[21],
                                                    'e-value': rsplit[30], 'scoring': rsplit[31]}}},
                                    'blast_gelijk': 'type_discrepantie',
                                 'hmm_gelijk': 'type_discrepantie'}
        with open("new_json.json", "w+") as new_json:
            json.dump(json_file, new_json)


def discrepantie_search():
    ffname = "1_R1_outputfile.tsv"
    rfname = "1_R2_outputfile.tsv"

    file_reader(ffname, rfname)



    # tax_dict2 = file_reader(fname2, sequentie="reverse")
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
