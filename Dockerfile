FROM ubuntu

RUN apt-get update --fix-missing
RUN apt install -y wget
RUN apt install -y python3.8

WORKDIR /app

# RUN apt-get install hmmer
RUN wget https://mafft.cbrc.jp/alignment/software/mafft_7.475-1_amd64.deb && dpkg -i mafft_7.475-1_amd64.deb 
RUN apt-get install -y hmmer

CMD ["./pipeline.sh"]