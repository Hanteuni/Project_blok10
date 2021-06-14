# Project Blok 10 
Github voor het project van blok 10: HMM en BLAST

# Project opzet
Om een beter idee te krijgen over de kwaliteit van BLAST annotatie is het idee ontstaan om deze te vergelijken met paired-sequence annotatie middels HMMs. Voor dit onderzoek zijn 2 datasets aangeleverd, een gecureerde 16S RNA dataset, en een 16S metagenomic paired-end reads dataset. Deze twee datasets doorlopen ieder een eigen vorm van pre-processing voordat de annotatie van beide datasets vergeleken kan worden. Vervolgens wordt bij de vergelijking van de annotatie gekeken naar discrepanties in de top 3 hits tussen de forward en reverse sequenties, en zijn de annotaties van BLAST en HMM tegen elkaar uitgezet. 

# Hoe run je de pipeline
- Note: Plaats in de Data map de metagenomics dataset (zie: Metagenomics_project_HMMs.csv), de 1_R1_outputfile.tsv en 1_R2_outputfile.tsv

De pipeline draait via een docker file, hierom is het slechts een kwestie van Docker installeren, downloaden, en de Docker project file aanroepen middels de volgende commando's:
docker build --tag <tag_name>
docker run -v ${PWD}:/app <tag_name>

In het geval de voorkeur uitgaat naar een instantie van de pipeline zonder gebruik van Docker voer dan de volgende stappen uit:
- Note: De pipeline maakt gebruik Python 3.8, en vereist dat MAFFT en HMMER geïnstalleerd zijn en draaien binnen een Ubuntu (16.04 en hoger) omgeving. 
pip install -r requirements
./pipeline.sh

# In welke map staat wat?
Fun fact: we gebruiken geen mapjes ;)
Data: hier komt de output van de pipeline



# Workflow



