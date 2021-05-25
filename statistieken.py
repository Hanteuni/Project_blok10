# Deze code maakt plots van de opgehaalde getallen.
# De getallen die gebruikt worden voor de plots worden aangemaakt bij het maken van de HMMs
# Het gaat hier dus over het aantal organismen per taxonomiehoogte

import matplotlib.pyplot as plt
import pandas as pd


def get_df(tax):
    """
    This function makes a pandas dataframe from a csv containing the amount of seqeunces per organism
    tax: The taxonomie level of wich you want to get the data frame
    This function is called from the main, for every taxonomy level, in an iterative way

    return: A datafram containf two colums in the follwing format: organism, amount
    """
    return pd.read_csv(tax + "/statistieken.csv", index_col=0)


def make_barplot_simple(df, log=False):
    """
    makes a simple bar plot, meaning plots the amount of sequences per organism.
    df: The data fram of wich a bar plot is made.

    The bar plots will be saved in the graph file with the name "[taxonomy level]bar.png"
    This function is called from the main per taxonomy level in an iterative way.
    """
    tax = df.index.name
    ax = df.plot(kind="bar", figsize=[15, 15], title=(
        "count of organisms per " + tax), logy=log)

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x()
                    * 0.995, p.get_height() * 1.005))
    plt.tight_layout()
    plt.savefig('graph/' + tax + 'bar.png')
    plt.show()


def make_barplot_increments(df, amount_increments=10):
    """
    Makes a bar plot baseds on increments,
    meaning makes [amount_increments] catogories based on the organism with the most sequences.
    example: most sequences = 100 with amount_increments = 4 the categories will be 0~25, 25~50, 50~75, 75~100.
    The bar displays the count of organisms which fall in these categories.
    df: The data fram of wich a bar plot is made.
    amount_increments: amount of increments plotted/ different catogories mande,
    will also correspond to the amount of bars in the plot.

    The bar plots will be saved in the graph file with the name "[taxonomy level]bar_increments.png"
    This function is called from the main per taxonomy level in an iterative way.
    """
    max = df["aantal"].max()
    stepsize = max / amount_increments
    lowerbound = 0
    upperbound = stepsize
    results = []
    tax = df.index.name
    index_text = []

    for i in range(amount_increments - 1):
        results.append(df[(df["aantal"] >= lowerbound)
                       & (df["aantal"] <= upperbound)])
        # print(df[(df["aantal"] >= lowerbound) & (df["aantal"] <= upperbound)])
        index_text.append(str(lowerbound)[:5] + " - " + str(upperbound)[:5])
        lowerbound = lowerbound + stepsize
        upperbound = upperbound + stepsize

    results.append(df[(df["aantal"] >= lowerbound)])
    # print(df[(df["aantal"] >= lowerbound)])

    index_text.append(str(lowerbound)[:5] + " -> ")

    index = [x for x in range(len(results))]
    value = [df.shape[0] for df in results]
    # print(value)

    plt.bar(index_text, value)
    plt.xticks(index, rotation=45)
    plt.title(tax + "\ncount of organisms per count of fasta's used to create HMM")
    plt.ylabel("count of different organisms")
    plt.xlabel("count of fasta's used to create HMM per " + tax +
               ",\nseperated in " + str(amount_increments) + " different catogories per count")

    for index, value in zip(index, value):
        plt.text(index, value, str(value))

    plt.tight_layout()
    plt.savefig('graph/' + tax + 'bar_increments.png')
    plt.show()


def bake_a_pie(df):
    """
    Makes a simple pie plot, meaning it shows the amount of sequences per organism in a pie chart.
    df: The data fram of wich a bar plot is made.

    The bar plots will be saved in the graph file with the name "[taxonomy level]pie.png"
    This function is called from the main per taxonomy level in an iterative way.
    """
    tax = df.index.name
    df.plot(y="aantal", kind="pie", figsize=[
            10, 10], title=tax, legend=False, labels=None)
    plt.axis('off')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('graph/' + tax + 'pie.png')
    plt.show()


def pie_cutoff(df, amount=5):
    """
    makes a pie chart with 2 pies splitting the data set in organisms with les then [amount] and higher then [amount].
    amount: the amount of sequences on which you want to split the data set.
    df: The data fram of wich a bar plot is made.

    The bar plots will be saved in the graph file with the name "[taxonomy level]pie_cutoff.png"
    This function is called from the main per taxonomy level in an iterative way.
    """
    tax = df.index.name
    lesser = df[df["aantal"] <= amount].shape[0]
    higher = df[df["aantal"] > amount].shape[0]
    plt.pie([lesser, higher], labels=["Lesser or equal than " +
            str(amount), "Higer than " + str(amount)], autopct='%1.1f%%')
    plt.title(tax)
    plt.savefig('graph/' + tax + 'pie_cutoff.png')
    plt.show()


if __name__ == '__main__':
    for tax in ["superkingdom", "phylum", "class", "family", "genus"]:
        df = get_df(tax)
        make_barplot_simple(df)
        make_barplot_increments(df)
        bake_a_pie(df)
        pie_cutoff(df)
