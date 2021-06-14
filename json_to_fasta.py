import json
import traceback

# Import van Biopython, as retrieved from the requirements.
from Bio.Seq import Seq
import sys


def json_to_fasta(file_json, forward):  # rename #TODO
    """
    This function loads the JSON file that was created before and creates a fasta file.
    file_json: The JSON file that's made into a fasta file.
    forward: True for the forward strand, False for the reverse strand.
    return: a fasta file that contains data from the json file.
    """
    # This will be a string that either says "forward" or "reverse".
    # The string is later used to save in the title and headers if the sequences are forward or reverse. 
    strand = ""
    # File writing errors are caught.
    try:
        # The JSON file is opened.
        with open(file_json) as json_file:
            data = json.load(json_file)
            # File writing errors when opening the output file are caught.
            try:
                # When forward is True the forward fasta file is being written.
                if forward:
                    strand = "forward"
                    # forward.fasta is created. This will be the output file.
                    f = open("data/" + strand + ".fasta", 'w')
                    # data is the json file, info is the header which is used as the key in the json file.
                    for info in data:
                        #TODO verengels maybe?
                        if str(data[info]["blast_gelijk"]):
                            # print(">" + info + "|{}".format(strand) + "\n"
                            #       + data[info]["forward_sequentie"]["sequentie"])
                            f.write(">" + info + "|{}".format(strand) + "\n"
                                    + data[info]["forward_sequentie"]["sequentie"] + "\n")
                        else:
                            print("blast is not equal to HMM, skipping")
                    f.close()
                else:
                    # When forward is False the reverse fasta file is being written.
                    strand="reverse"
                    # forward.fasta is created. This will be the output file
                    f=open(strand + ".fasta", 'w')
                    # data is the json file, info is the header which is used as the key in the json file.
                    for info in data:
                        #TODO moet hier niet ook een controle op discrepanties?
                        # A file is created, which looks like this:
                        # >header|reverse\n
                        # sequence
                        # print(">" + info + "|{}".format(strand) + "\n"
                        #       + data[info]["reverse_sequentie"]["sequentie"])
                        # The sequence is forward oriented, so it needs to be reversed and made complementary.
                        sequentie=Seq(
                            data[info]["reverse_sequentie"]["sequentie"]).reverse_complement()
                        f.write(">" + info + "|{}".format(strand) + "\n"
                                + str(sequentie) + "\n")
                    f.close()
            except FileNotFoundError:
                print("fasta file (to write to) could not be found.")
    except FileNotFoundError:
        print("json file was not found.")
    except IOError:
        print("File could not be opened. Check your permissions", traceback.print_exc())


if __name__ == '__main__':
    # The JSON file that will be made into a fasta file
    doom_json_file = "./ALL_BLAST.json"
    # The function that makes the fasta file is called here
    json_to_fasta(doom_json_file, forward = bool(sys.argv[1]))
    print("Done, file was filled")
