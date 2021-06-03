class scoring_system:

    def __init__(self, file="All_HMM.json", type="hmms", tax_height="class"):
        self.file = file
        self.type = type
        self.tax_height = tax_height

        number_of_simularitys = json_splitter_i_guess(self.file, self.type, self.tax_height)


def json_splitter_i_guess(file, tool, tax_height):
    import json
    json_file = json.loads(open(file).read())
    for i in json_file:
        # json [forward/reverse][taxonomie _ hmms/blast _ tax-niveau
        forward_taxonomy_levels = json_file[i]["forward_sequentie"]["taxonomie_{}_{}".format(tool, tax_height)]
        reverse_taxonomy_levels = json_file[i]["reverse_sequentie"]["taxonomie_{}_{}".format(tool, tax_height)]
        # TODO doom.json omscrijven naar een zelfde format als ALL_HMM
        discrep = check(forward_taxonomy_levels, reverse_taxonomy_levels, tax_height)
    #     discrep = hoeveelheid overeenkomende organismen
    #     TODO aanpassen waar we willen opslaan hoe willen opslaan

        print(discrep)


def check(forward_taxonomy_levels, reverse_taxonomy_levels, tax_height):
    forward_taxonomie, reverse_taxonomie = [], []
    for i in range(1, 4):
        forward_taxonomie.append(forward_taxonomy_levels["tax{}_{}".format(i, tax_height)]["annotatie"])
        reverse_taxonomie.append(reverse_taxonomy_levels["tax{}_{}".format(i,tax_height)]["annotatie"])
    # forward_taxonomie, reverse_taxonomie = ["Clostridia", "Thermotogae", "Clostridia"], \
    #                                        ["Clostridia", "Clostridia", "Thermotogae"]
    number_of_simular_taxos = set(forward_taxonomie).intersection(set(reverse_taxonomie))
    return len(number_of_simular_taxos)


test = scoring_system(file="All_HMM.json", type="hmms", tax_height="class")
