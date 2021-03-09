import os
import numpy
import matplotlib as plt
# professionals have standards


def get_files():
    """
    :return: enters the file_to_fasta function in which it reads and writes.
    """
    # dir = input("")
    direc = "/home/rutger/blok10"
    directory_files = os.listdir(direc)

    for tsv in directory_files:
        if tsv.endswith(".tsv"):
            file_to_fasta(tsv)


def file_to_fasta(file):
    """
    Functionality:
    :param file: takes a .tsv file with either the forward or reverse reads.
    :return: output is a fasta file with ID and corresponding raw sequence.
    """
    fasta_file = file.strip(".tsv") + "_rut.fasta"

    if os.path.exists("./"+fasta_file):
        with open(file) as file, open(fasta_file, "w+") as output_fasta:
            file.readline()
            for line in file:
                line = line.split("\t")
                output_fasta.write(">" + str(line[0]) + "\n" + line[2] + "\n")
    else:
        with open(file) as file, open(fasta_file, "a") as output_fasta:
            # fasta_file.truncate(0)
            file.readline()
            for line in file:
                line = line.split("\t")
                output_fasta.write(">" + str(line[0]) + "\n" + line[2] + "\n")


if __name__ == '__main__':
    get_files()
    print("done")
