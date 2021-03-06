class ScoringSystem:
    """
    a scoring system which takes a hmm json file or a blas json file. ad calculates discrepancies between them.
    """

    def __init__(self, file="All_HMM.json", type="hmms", tax_height="class"):
        """
        file: The json file containing the hmms or the blast results, these are generated by: parse_hmm.py and
        discrepantie_earch.py
        type: the type of file, so hmm or blast. same files as mentioned above
        tax_height: the taxonomy level on wich discrepancies are scored.
        """
        # save the init args
        self.file = file
        self.type = type
        self.tax_height = tax_height

    def __compute_similarity(self, output_type: str = "dict"):
        """
        computes the similarity between the taxonomy in the json files on self.tax_height per forward and reverse read
        couple. if a taxonomy is present in a forward and a reverse read then ist's counted as a similarity.
        output_type: kind of output which is produced, either dict format or string
            example: dict = [read id: similarities], list = [similarities]
        """
        import json
        res_dict = {}
        json_file = json.loads(open(self.file).read())
        # loop trough json file
        for id in json_file:
            similarities = 0
            forward_taxonomie, reverse_taxonomie = [], []
            # for all hits append annotation to temporary list
            for i in range(1, 4):
                forward_taxonomie.append(json_file[id]["forward_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
                                         [f"tax{i}_{self.tax_height}"]["annotatie"])
                reverse_taxonomie.append(json_file[id]["reverse_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
                                         [f"tax{i}_{self.tax_height}"]["annotatie"])

            # this is used so the taxonomy results from blast and hmm look more similar
            new_forward = self.__convert_to_hmm_standerd(forward_taxonomie)
            new_reverse = self.__convert_to_hmm_standerd(reverse_taxonomie)

            # calculates similarities
            for tax in new_forward:
                if tax in new_reverse:
                    similarities += 1

            res_dict[id] = similarities

        if output_type == "list":
            return list(res_dict.values())
        else:
            return res_dict

    def __convert_to_hmm_standerd(self, taxonomy):
        """
        converts the taxonomy results to a standardised format such tat the same taxonomy in blast is
        converted into separate names.
        taxonomy: a list containing the taxonomy retrieved from the json file in the format ["tax1", "tax2", "tax3"]
        returns a standardised taxonomy
            example: ["tax1", "tax2", "tax3"]
        """
        new_taxonomy = []
        counter = 0
        # loop trough taxonomy
        for i in taxonomy:
            if i not in new_taxonomy:
                new_taxonomy.append(i)
            else:
                # if there is a duplicate append it with a number behind it
                new_taxonomy.append(i + str(counter))
                counter += 1
        return new_taxonomy

    def __one_on_one(self, output_type: str = "dict"):
        """
        computes the similarity between the taxonomy in the json files on self.tax_height per forward and reverse read
        couple. if a taxonomy is present in a forward and a reverse read and are in the same hit it's counted as a similarity.
        output_type: kind of output which is produced, either dict format or string
            example: dict = [read id: similarities], list = [similarities]
        """
        import json
        res_dict = {}
        json_file = json.loads(open(self.file).read())
        # loop troug json file
        for id in json_file:
            similarities = 0
            forward_taxonomie, reverse_taxonomie = [], []
            for i in range(1, 4):
                # for all hits append annotation to temporary list
                forward_taxonomie.append(json_file[id]["forward_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
                                         [f"tax{i}_{self.tax_height}"]["annotatie"])
                reverse_taxonomie.append(json_file[id]["reverse_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
                                         [f"tax{i}_{self.tax_height}"]["annotatie"])
            # compare annotatie per posistion
            for i in range(len(forward_taxonomie)):
                if forward_taxonomie[i] == reverse_taxonomie[i]:
                    similarities += 1

            res_dict[id] = similarities

        if output_type == "list":
            return list(res_dict.values())
        else:
            return res_dict

    def get_similarities_list(self):
        return self.__compute_similarity("list")

    def get_similarities_dict(self):
        return self.__compute_similarity()

    def get_one_on_one_list(self):
        return self.__one_on_one("list")

    def get_one_on_one_dict(self):
        return self.__one_on_one()

    # def get_set_list(self):
    #     self.__json_splitter_i_guess()
    #     return self.__json_splitter_i_guess("list")
    #
    # def get_set_dict(self):
    #     return self.__json_splitter_i_guess()

# depricated old functions
# def __dicrepancies_using_sets(self, output_type: str = "dict"):
#     """
#     scores discrepancies using sets, this function is depricated but gives
#     """
#     import json
#     res_dict = {}
#     json_file = json.loads(open(self.file).read())
#
#     for i in json_file:
#         # json [forward/reverse][taxonomie _ hmms/blast _ tax-niveau
#         forward_taxonomy_levels = json_file[i]["forward_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
#         reverse_taxonomy_levels = json_file[i]["reverse_sequentie"][f"taxonomie_{self.type}_{self.tax_height}"]
#         discrep = self.__check(forward_taxonomy_levels, reverse_taxonomy_levels, self.tax_height)
#         # discrep = hoeveelheid overeenkomende organismen
#         res_dict[i] = discrep
#
#     if output_type == "list":
#         return list(res_dict.values())
#     else:
#         return res_dict
#
# def __check(self, forward_taxonomy_levels, reverse_taxonomy_levels, tax_height):
#     forward_taxonomie, reverse_taxonomie = [], []
#     for i in range(1, 4):
#         forward_taxonomie.append(forward_taxonomy_levels["tax{}_{}".format(i, tax_height)]["annotatie"])
#         reverse_taxonomie.append(reverse_taxonomy_levels["tax{}_{}".format(i, tax_height)]["annotatie"])
#         # forward_taxonomie, reverse_taxonomie = ["Clostridia", "Thermotogae", "Clostridia"], \
#         #                                        ["Clostridia", "Clostridia", "Thermotogae"]
#         number_of_simular_taxos = set(forward_taxonomie).intersection(set(reverse_taxonomie))
#
#     return len(number_of_simular_taxos)
