import json
import traceback
from Bio.Seq import Seq


def json_to_fasta(file_json, forward):     #rename
    strand = ""
    try:
        with open(file_json) as json_file:
            data = json.load(json_file)
            try:
                if forward:
                    strand = "forward"
                    f = open(strand + ".fasta", 'w')
                    for info in data:
                        if str(data[info]["blast_gelijk"]):
                            pass
                            # print(">" + info + "|{}".format(strand) + "\n"
                            #       + data[info]["forward_sequentie"]["sequentie"])
                            # f.write(">" + info + "|{}".format(strand) + "\n"
                            #         + data[info]["forward_sequentie"]["sequentie"] + "\n")
                        else:
                            # continue
                            print("blast is not equal to HMM, skipping")
                    f.close()
                else:
                    strand = "reverse"
                    f = open(strand + ".fasta", 'w')
                    for info in data:
                        print(">" + info + "|{}".format(strand) + "\n"
                              + data[info]["reverse_sequentie"]["sequentie"])
                        sequentie = Seq(data[info]["reverse_sequentie"]["sequentie"]).reverse_complement()
                        f.write(">" + info + "|{}".format(strand) + "\n"
                                + str(sequentie) + "\n")
                    f.close()
            except FileNotFoundError:
                print("fasta file (to write to) could not be found.")
    except FileNotFoundError:
        print("json file was not found.")
    except IOError:
        print("problem opening shit", traceback.print_exc())


if __name__ == '__main__':
    doom_json_file = "./DOOM.json"
    json_to_fasta(doom_json_file, forward=False)
    print("Done, file was filled")