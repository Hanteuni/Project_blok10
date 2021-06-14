# Ubuntu as base image
FROM ubuntu

# Setting up the enviroment
RUN apt-get update --fix-missing
RUN apt install -y wget
RUN apt install -y python3.8
RUN apt-get install -y python3-pip

# Defining a working enviroment
WORKDIR /app

# Installing dependencies
RUN wget https://mafft.cbrc.jp/alignment/software/mafft_7.475-1_amd64.deb && dpkg -i mafft_7.475-1_amd64.deb 
RUN apt-get install -y hmmer

# Starting the pipeline
CMD ["./pipeline.sh"]
