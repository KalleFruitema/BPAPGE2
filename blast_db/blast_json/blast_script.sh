wget "http://ftp.ensembl.org/pub/release-110/fasta/panthera_pardus/cds/Panthera_pardus.PanPar1.0.cds.all.fa.gz" -O blast_db/pan_par_proteome.fa.gz
gunzip blast_db/pan_par_proteome.fa.gz
makeblastdb -dbtype nucl -in blast_db/pan_par_proteome.fa
blastn -db blast_db/pan_par_proteome.fa -query blast_db/seq2.fa -outfmt 13 -out blast_db/blast_json/blast_results.json