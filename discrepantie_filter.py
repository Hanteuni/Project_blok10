import json, tqdm


def file_reader(ffname, rfname, ):
    json_file = {}

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

            disc_type = discrepantie_search(tax_dict1,tax_dict2)
            json_file[fsplit[0]] = {'forward_sequentie':{'sequentie': fsplit[2], 'taxonomie_blast': {'tax1':
                                    {'annotatie': fsplit[10],'e-value': fsplit[19],'scoring': fsplit[20]},
                                      'tax2': {'annotatie': fsplit[21],'e-value': fsplit[30],'scoring': fsplit[31]}}},
                                    'reverse_sequentie': {'sequentie': rsplit[2], 'taxonomie_blast':
                                    {'tax1':{'annotatie': rsplit[10],'e-value': rsplit[19],'scoring': rsplit[20]},
                                    'tax2': {'annotatie': rsplit[21], 'e-value':rsplit[30],'scoring':rsplit[ 31]}}},
                                    'blast_gelijk': disc_type,
                                    'hmm_gelijk': 'type_discrepantie'}
        print("preparing transfer to json file")
        with open("DOOM.json", "w+") as new_json:
            print("uploading the jason file... ")
            json.dump(json_file, new_json)
            print("file is done")


def discrepantie_search(tax_dict1, tax_dict2):
    hdrs = ["Domain", "Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
    disc_type = ""
    for key in tax_dict1:
        if tax_dict1.get(key) == "" and tax_dict2.get(key) == "":
            disc_type = "both reads empty"
        if tax_dict1.get(key) != tax_dict2.get(key):
            if tax_dict1.get(key) == "":
                disc_type = "forward read empty"
            elif tax_dict2.get(key) == "":
                disc_type = "reverse read empty"
                # hij kijkt alleen naar de eerste hit en niet naar de 2e en 3e
            elif tax_dict1.get(key)[0] != tax_dict2.get(key)[0]:
                disc_type = tax_splitter(tax_dict1, tax_dict2, key, hdrs)
    return disc_type
    # counter = {} # yo pik we hebben jullie werk gedaan ook al was het voor bugfixing +1 voor chrissie
    # for key in disc_dict:
    #     if disc_dict.get(key) in counter:
    #         counter[disc_dict.get(key)] += 1
    #     else:
    #         counter[disc_dict.get(key)] = 1


def tax_splitter(tax_dict1, tax_dict2, key, hdrs):
    tax_set1 = set(tax_dict1.get(key)[0].split("|"))
    tax_set2 = set(tax_dict2.get(key)[0].split("|"))
    difference = tax_set1 - tax_set2
    return hdrs[len(difference) - 1]


def empty_json():
    old_json_file = open("DOOM.json", "r+")
    # old = json.load(old_json_file)

    old_json_file.truncate(0)
    new_json_file = open("back_up.json", "r+")
    new = json.load(new_json_file)
    json.dump(new, old_json_file)
    old_json_file.close()


if __name__ == '__main__':
    # empty_json()
    ffname = "1_R1_outputfile.tsv"
    rfname = "1_R2_outputfile.tsv"
    file_reader(ffname, rfname)
