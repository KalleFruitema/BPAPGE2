wget "http://ftp.ensembl.org/pub/release-110/fasta/panthera_pardus/pep/Panthera_pardus.PanPar1.0.pep.all.fa.gz"
gunzip Panthera_pardus.PanPar1.0.pep.all.fa.gz
makeblastdb -dbtype prot -in Panthera_pardus.PanPar1.0.pep.all.fa
blastx -db Panthera_pardus.PanPar1.0.pep.all.fa -query seq2.fa -outfmt 13 -out blast_results.json
