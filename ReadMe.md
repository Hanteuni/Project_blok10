Dit bevat mijn de pipeline en wat aangepaste code.\
janne.faste moet Han zijn testbestand worden.\
Verder staan alle bestanden er die nodig zijn!\

# Aanroep via Docker
Zorg dat alle data bestanden in de map "data" zitten. Hierin moeten dus janne.csv, janne.fasta en HANBC Metagenomics project HMMs v01.xlsx staan. \
Voer vervolgens de onderstaande commando's uit. Hiervoor is een werkende Docker Desktop nodig, verder hoeft niets geinstalleerd.\
Het argument om de working directory te krijgen kan verschillen per commandline. Dit is hoe het in Powershell uitgevoerd moet worden.
1. `docker build --tag teuntje .`
2. `docker run -v ${PWD}:/app teuntje`