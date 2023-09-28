wget "http://ftp.ensembl.org/pub/release-110/fasta/panthera_pardus/cds/Panthera_pardus.PanPar1.0.cds.all.fa.gz"
gunzip Panthera_pardus.PanPar1.0.cds.all.fa.gz
makeblastdb -dbtype nucl -in Panthera_pardus.PanPar1.0.cds.all.fa
blastn -db Panthera_pardus.PanPar1.0.cds.all.fa -query ../seq2.fa -outfmt 13 -out blast_results.json