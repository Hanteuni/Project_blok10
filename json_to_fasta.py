import json
import traceback

# Import van Biopython, zoals verkregen via de requirements
from Bio.Seq import Seq


def json_to_fasta(file_json, forward):  # rename #TODO
    """
    Deze functie laad het eerder aangemaakte JSON bestand in en maakt hier een Fasta bestand van.
    file_json: Het JSON bestand waarvan een Fasta file wordt gemaakt
    forward: True als de forward strand wordt gebruikt, False voor de reverse strand
    return: een geschreven fasta bestand.
    """
    # Dit wordt een string die ofwel forward, of reverse is.
    # Dit wordt later gebruikt om op te slaan in de titel en de header welke strand het is.
    strand = ""
    # Bestandschrijffouten worden afgevangen
    try:
        # Het JSON bestand wordt geopend
        with open(file_json) as json_file:
            data = json.load(json_file)
            # Een bestandschrijffout wordt afgevangen, voor als het schrijfbestand niet kan worden geopend.
            try:
                # forward is True of False, als het True is wordt de forward strand weggeschreven.
                if forward:
                    strand = "forward"
                    # forward.fasta wordt aangemaakt of geleegd. Hier worden straks de sequenties en headers naar weggeschreven.
                    f = open(strand + ".fasta", 'w')
                    # data is het json bestand, info is de header die als key wordt gebruikt.
                    for info in data:
                        if str(data[info]["blast_gelijk"]):
                            print(">" + info + "|{}".format(strand) + "\n"
                                  + data[info]["forward_sequentie"]["sequentie"])
                            f.write(">" + info + "|{}".format(strand) + "\n"
                                    + data[info]["forward_sequentie"]["sequentie"] + "\n")
                        else:
                            print("blast is not equal to HMM, skipping")
                    f.close()
                else:
                    # forward is True of False, als het False is wordt de reverse strand weggeschreven.
                    strand="reverse"
                    # reverse.fasta wordt aangemaakt of geleegd. Hier worden straks de sequenties en headers naar weggeschreven.
                    f=open(strand + ".fasta", 'w')
                    # data is het json bestand, info is de header die als key wordt gebruikt.
                    for info in data:
                        #TODO moet hier niet ook een controle op discrepanties?
                        # Er wordt een bestand gemaakt die er als volgt uit ziet:
                        # >header|reverse\n
                        # sequentie
                        print(">" + info + "|{}".format(strand) + "\n"
                              + data[info]["reverse_sequentie"]["sequentie"])
                        # Omdat de sequentie als een forward sequentie is opgeslagen moet deze reverse complementair gemaakt worden.
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
    doom_json_file="./DOOM.json"
    # The function that makes the fasta file is called here
    json_to_fasta(doom_json_file, forward = False)
    print("Done, file was filled")
