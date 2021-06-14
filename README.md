# Project Blok 10 
Github voor het project van blok 10: HMM en BLAST

# Project opzet
Om een beter idee te krijgen over de kwaliteit van BLAST annotatie is het idee ontstaan om deze te vergelijken met paired-sequence annotatie middels HMMs. Voor dit onderzoek zijn 2 datasets aangeleverd, een gecureerde 16S RNA dataset, en een 16S metagenomic paired-end reads dataset. Vervolgens wordt bij de vergelijking van de annotatie gekeken naar discrepanties in de top 3 hits tussen de forward en reverse sequenties, en zijn de annotaties van BLAST en HMM met elkaar vergeleken. 

# Hoe run je de pipeline
- Note: Plaats in de Data map de metagenomics dataset (zie: Metagenomics_project_HMMs.csv), de 1_R1_outputfile.tsv en 1_R2_outputfile.tsv

De pipeline draait via een Docker file, hierom is het slechts een kwestie van Docker installeren, downloaden, en de Docker project file aanroepen middels de volgende commando's:
docker build --tag <tag_name>
docker run -v ${PWD}:/app <tag_name>

In het geval de voorkeur uitgaat naar een instantie van de pipeline zonder gebruik van Docker voer dan de volgende stappen uit:
- Note: De pipeline maakt gebruik Python 3.8, en vereist dat MAFFT en HMMER geïnstalleerd zijn en draaien binnen een Ubuntu (16.04 en hoger) omgeving. 
pip install -r requirements
./pipeline.sh

# Indeling van files
In het overzicht van de files op de github vindt men alle functies waarmee het project doorlopen wordt. De 
Data: hier komt de output van de pipeline
Overige mapjes? ~~~~~~~~~~~~~~~~


# Workflow
De flow van processen in de pipeline valt in 3 stappen uit te leggen.

1: Input data bevattende rauwe 16S RNA data en een 16S metagenomic paired-end reads dataset zijn ontvangen.

2: De verkregen data wordt middels data preprocessing klaar gemaakt om met elkaar vergeleken te worden. 
  - Tijdens pre-processing wordt de gecureerde 16S data geparsed naar de HMM database en wordt deze gebruikt om HMMs te trainen en filteren. Hierna worden de HMMs weggeschreven naar een JSON file met enkel HMMs.
  - De andere 16S metagenomic paired-end reads dataset wordt gefilterd op discrepanties, en de BLAST resultaten worden naar een JSON file geschreven. Vervolgens wordt van de gefilterde data fasta bestanden gemaakt die tevens gebruikt worden voor het maken en filteren van HMMs. Uiteindelijk wordt ook deze data naar de JSON file met enkel HMMs geschreven. 

3: De JSON files worden uiteindelijk gebruikt om middels Python een vergelijking uit te voeren op de discrepanties, en hiervan worden de resultaten gevisualiseerd. 


