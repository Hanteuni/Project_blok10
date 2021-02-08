import re


def parse_tsv(tsv):
    """Zet tsv in een dictionary

    :param tsv: -str- naam tsv bestand
    :return:
    """
    # Declareer variabelen
    tsv_dic = {}
    with open(tsv) as inFile:
        first_line = inFile.readline().split("\t")
        taxidx = first_line.index("taxonomy")
        for line in inFile:
            line = line.split("\t")
            tsv_dic[line[0]] = line[taxidx]

    return tsv_dic


def prep_tax_in_values(tax_dic):
    """taxonomy splitten, checken of de hele rits aanwezig is
    (p, c, o, f, g, sp, str) deze data preppen voor later gebruik

    :param tax_dic: dict - taxonomy dictionary
    :return: {header: [int, p, c, o, f, g, sp, str]}
    """
    improved_dict = {}
    re_str = ["p", "c", "o", "f", "g", "sp", "str"]
    for key, value in tax_dic.items():
        temp_list = []
        temp_list.append(value.split("_")[0])
        for reg in re_str:
            regex = "(_{}\|)[a-z|A-Z|0-9]*".format(reg)
            match = re.search(regex, value)
            if match:
                temp_list.append(match.group().split("|")[-1])
            else:
                temp_list.append("NE")

        improved_dict[key] = temp_list
    return improved_dict


def combine_fwd_rvs(fwd, rvs):
    """Combineren van de forward en reverse in een dictionary. De
    taxonomy wordt hierbij opgeslagen in twee lijsten per key. Zie
    return statement

    :param fwd:
    :param rvs:
    :return: - {header: [[tax_fwd], [tax_rvs]],
    header: [[tax_fwd], [tax_rvs]]}
    """
    combine_dic = {}
    for key in fwd.keys():
        combine_dic[key] = [fwd[key], rvs[key]]

    return combine_dic


def compare_fwd_rvs(fw_and_rv_dic):
    """Welke taxonomy komen niet overeen en welke komen niet overeen

    :param fw_and_rv_dic: {header: [[tax_fwd], [tax_rvs]],
    header: [[tax_fwd], [tax_rvs]]}
    """
    ongelijk = []
    for key, value in fw_and_rv_dic.items():
        if value[0][0] != value[1][0]:
            ongelijk.append(key)

    aantal_ongelijk = len(ongelijk)
    aantal_gelijk = len(fw_and_rv_dic.keys()) - aantal_ongelijk

    return ongelijk, aantal_gelijk, aantal_ongelijk


def point_system(fw_and_rv_dic):
    """Bereken aantal punten. Bij 1 overeenkomst 1 punt, bij 2 2 etc.

    :param fw_and_rv_dic:
    :return: points - dict- : {header: punt, header: punt}
    """
    points = {}
    for key, value in fw_and_rv_dic.items():
        p = 0
        # print(len(value[0]), len(value[1]))
        for i in range(len(value[0])):
            if value[0][i] == value[1][i]:
                p += 1
        points[key] = p

    return


if __name__ == '__main__':
    # Declareer bestanden
    fwd = "3_R1_outputfile.tsv"
    rvs = "3_R2_outputfile.tsv"

    # Inlezen van tsv bestanden forward en reverse reads
    fwd_dic = parse_tsv(fwd)
    rvs_dic = parse_tsv(rvs)

    # Afwerking inlezen bestanden --> overzichtelijk maken
    fwd_dic = prep_tax_in_values(fwd_dic)
    rvs_dic = prep_tax_in_values(rvs_dic)

    # Combineer de resultaten
    combined_dic = combine_fwd_rvs(fwd_dic, rvs_dic)

    # Lijsten met wat statistieken
    ongelijk, aantal_gelijk, aantal_ongelijk = \
        compare_fwd_rvs(combined_dic)

    points = point_system(combined_dic)