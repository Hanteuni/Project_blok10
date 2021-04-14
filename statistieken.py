import matplotlib.pyplot as plt
import pandas as pd


def get_df(tax):
    return pd.read_csv(tax + "/statistieken.csv", index_col=0)


def make_barplot_simple(df, log=False):
    tax = df.index.name
    ax = df.plot(kind="bar", figsize=[15, 15], title=("count of organisms per " + tax), logy=log)

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() * 0.995, p.get_height() * 1.005))
    plt.tight_layout()
    plt.savefig('graph/' + tax + 'bar.png')
    plt.show()


def make_barplot_increments(df, steps=10):
    max = df["aantal"].max()
    stepsize = max / steps
    lowerbound = 0
    upperbound = stepsize
    results = []
    tax = df.index.name
    index_text = []

    for i in range(steps-1):
        results.append(df[(df["aantal"] >= lowerbound) & (df["aantal"] <= upperbound)])
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
    plt.title( tax + "\ncount of organisms per count of fasta's used to create HMM")
    plt.ylabel("count of different organisms")
    plt.xlabel("count of fasta's used to create HMM per " + tax + ",\nseperated in " + str(steps) + " different catogories per count")

    for index, value in zip(index, value):
        plt.text(index, value, str(value))

    plt.tight_layout()
    plt.savefig('graph/' + tax + 'bar_increments.png')
    plt.show()



def bake_a_pie(df):
    tax = df.index.name
    df.plot(y="aantal", kind="pie", figsize=[10, 10], title=tax, legend=False, labels=None)
    plt.axis('off')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig('graph/' + tax + 'pie.png')
    plt.show()


def pie_percentage(df, amount=5):
    tax = df.index.name
    lesser = df[df["aantal"] <= amount].shape[0]
    higher = df[df["aantal"] > amount].shape[0]
    plt.pie([lesser, higher], labels=["Lesser or equal than " + str(amount), "Higer than " + str(amount)], autopct='%1.1f%%')
    plt.title(tax)
    plt.savefig('graph/' + tax + 'pie_cutoff.png')
    plt.show()


if __name__ == '__main__':
    for tax in ["superkingdom", "phylum", "class", "family", "genus"]:
        df = get_df(tax)
        bake_a_pie(df)
