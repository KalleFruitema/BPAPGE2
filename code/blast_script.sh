#!/bin/bash

# Date: 8/12/2023
# Author: Kalle Fruitema
# Dit script download het proteoom van panthera pardus van ENSEMBL,
# unzipt dit, maakt er een database van, en blast data/seq2.fa
# tegen deze database

# Usage: $ ./blast_script.sh

# download proteoom van panthera pardus vanaf ftp.ensembl,org
wget "http://ftp.ensembl.org/pub/release-110/fasta/panthera_pardus/cds/Panthera_pardus.PanPar1.0.cds.all.fa.gz" -O blast_db/pan_par_proteome.fa.gz

# unpackt het gedownloadde proteoom
gunzip blast_db/pan_par_proteome.fa.gz

# maakt een blast database van nucleotiden met het proteoom
makeblastdb -dbtype nucl -in blast_db/pan_par_proteome.fa

# blastn voor elke sequentie in data/seq2.fa tegen de database
# van het proteoom, output is voor elke sequentie in data/seq2.fa
# een apart json bestand voor resultaat in data/blast_results_json/
blastn -db blast_db/pan_par_proteome.fa -query data/seq2.fa -outfmt 13 -out data/blast_results_json/blast_results.json
