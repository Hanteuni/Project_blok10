import collections

from scoring_system import *
import matplotlib.pyplot as plt
import sys


def create_bar_chart(res_list: list, title: str, xlabel: str, ylabel: str):
    """
    creates a basic bar chart
    res_list: list provided bij scoring system.py
    title: Title of the bar plot
    xlabel: the lable of the x as
    ylabel: the lable of the y as
    """

    dict = count_occeurence(res_list)
    for i in res_list:
        if i in dict:
            dict[i] = (dict[i] +1)
        if i not in dict:
            dict[i] = 1
    # dict = Counter(res_list)
    # print(dict.keys(), dict.values())
    plt.bar(dict.keys(), dict.values())

    for index, value in zip(dict.keys(), dict.values()):
        plt.text(index-0.20, value, str(value))

    # print(list(dict.keys()))
    plt.xticks(list(dict.keys()))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig("data/" + title + '.png')


def count_occeurence(res_list):
    """
    count occurrence of amount of similarities
    res_list: the list with the amount of similarities
    """
    dict = {}
    for i in res_list:
        if i in dict:
            dict[i] = (dict[i] + 1)
        if i not in dict:
            dict[i] = 1

    return collections.OrderedDict(sorted(dict.items()))


def grouped_bar_chart(hmm_list, blast_list, title):
    """
    makes a grouped bar chart of two lists from scoring system.py
    hmm_list: the scoring system list
    title: the tile of the bar chart
    """
    import matplotlib.pyplot as plt
    import numpy as np

    hmm = count_occeurence(hmm_list)
    blast = count_occeurence(blast_list)

    labels = [0, 1, 2, 3]
    labels_hmm = hmm.keys()
    labels_blast = blast.keys()

    x_hmm = np.arange(len(labels_hmm))
    # the label locations
    x_blast = np.arange(len(labels_blast))
    # the width of the bars
    width = 0.35

    print(x_blast, x_hmm)
    print(blast.values(), hmm.values())

    fig, ax = plt.subplots()
    rects1 = ax.bar(x_hmm - width / 2, hmm.values(), width, label='HMM', color="purple")
    rects2 = ax.bar(x_blast + width / 2, blast.values(), width, label='BLAST')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Hoeveelheid reads per overeenkomst')
    ax.set_xlabel('Hoeveelheid overeenkomsten tussen forward en reverse read annotatie')
    ax.set_title(title)
    ax.set_xticks(labels)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    plt.savefig( "data/"+ title + '.png')

if __name__ == '__main__':
    print("loading scores")
    # hmm_json = sys.argv[1]
    # blast_json = sys.argv[2]
    hmm_json = "All_HMM.json"
    blast_json = "All_BLAST.json"

    scoring_system_hmm = ScoringSystem(file=hmm_json, type="hmms", tax_height="class")

    res_list_hmm = scoring_system_hmm.get_similarities_list()
    # create_bar_chart(res_list_hmm, title="HMM's overeenkomsten met compensatie voor duplicaten",
    #                  xlabel="Hoeveelheid vereenkomsten tussen forward en reverse read annotatie",
    #                  ylabel="Hoeveelheid reads per overeenkomst")

    res_list_hmm_one = scoring_system_hmm.get_one_on_one_list()
    # create_bar_chart(res_list_hmm_one, title="HMM's overeenkomsten per positie",
    #                  xlabel="Overeenkomsten tussen forward en reverse reads",
    #                  ylabel="Hoeveelheid reads per overeenkomst"
    #                  )

    scoring_system_blast = ScoringSystem(file=blast_json, type="blast", tax_height="class")

    res_list_blast_list = scoring_system_blast.get_similarities_list()
    # create_bar_chart(res_list_blast_list, title="BLAST overeenkomsten met compensatie voor duplicaten",
    #                  xlabel="Overeenkomsten tussen forward en reverse reads",
    #                  ylabel="Hoeveelheid reads per overeenkomst")

    res_list_blast_one = scoring_system_blast.get_one_on_one_list()
    # create_bar_chart(res_list_blast_one, title="BLAST overeenkomsten per positie",
    #                  xlabel="Overeenkomsten tussen forward en reverse reads",
    #                  ylabel="Hoeveelheid reads per overeenkomst")

    grouped_bar_chart(res_list_hmm, res_list_blast_list, "overeenkomsten met compensatie voor duplicaten grouped bar")
    grouped_bar_chart(res_list_hmm_one, res_list_blast_one, "overeenkomsten per positie grouped bar")

