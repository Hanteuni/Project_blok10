import os


def read_files(dir):
    """
    reads all tsv files in the given directory
    :param dir: the directory
    """
    directory_files = [file for file in os.listdir(dir) if ".tsv" in file]

    for tsv in directory_files:
        tsv_to_fasta(dir+tsv)


def tsv_to_fasta(tsv):
    """
    converts tsv to fasta file
    :param tsv: the tsv file to convert
    """
    fasta_file = tsv.replace(".tsv", ".fasta")

    with open(tsv) as csv, open(fasta_file, "w+") as output_fasta:
        csv.readline()
        for line in csv:
            list_line = line.split("\t")
            output_fasta.write(">" + list_line[0] + "\n" + list_line[2] + "\n")
    csv.close()
    output_fasta.close()


if __name__ == '__main__':

    #  geef input folder
    dir = "blast_resultaten/"

    read_files(dir)

