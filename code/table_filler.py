import os
import json
from pprint import pprint
from Bio import SeqIO


# Entrez.api_key = "MyAPIKey"
# Entrez.email = "kallefruitema@gmail.com"


# deze functie werkt helemaal goed
def fill_table_brokstuk(cursor):
    with open('blast_db/seq2.fa') as file:
        inhoud = file.read().strip().split('\n')
    fasta_dict = {}
    for i, line in enumerate(inhoud):
        if line[0] == '>': 
            fasta_dict.update({
                line: inhoud[i+1]
            })
    for key_val in fasta_dict.items():
        sql = """INSERT INTO BROKSTUK(brokstuk_header, brokstuk_sequence)
        VALUES(%s, %s)"""
        cursor.execute(sql, key_val)
    print("Brokstuk table filled!")


# deze functie werkt, alleen de GENE tabel moet eerst gevuld worden vanwege foreign keys
def fill_table_alignment(cursor, data):
    sql = """INSERT INTO ALIGNMENT(brokstuk_header, alignment_ID, ENSEMBL_gene_ID, 
    alignment_length, e_value, bit_score, percentage_identity, gaps,
    mismatches, startpos_hit, endpos_hit)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for line in data:
        cursor.execute(sql, line)
    print("Alignment table filled!")

# ik loop vast op de data hiervan krijgen
def fill_table_gene(cursor, data):
    sql = """INSERT INTO GENE(ENSEMBL_gene_ID, gene_name, 
    gene_sequence, gene_description)
    VALUES(%s, %s, %s, %s)"""
    for line in data:
        cursor.execute(sql, line)
    print("Gene table filled!")


def parse_blast(file_list):
    # os.popen('sh blast_db/blast_json/blast_script.sh')
    alignment_data = []
    gene_data = set()
    blast_db = []
    path = r"blast_db\blast_json\Panthera_pardus.PanPar1.0.cds.all.fa"
    for seq_record in SeqIO.parse(path, "fasta"):
        blast_db.append(seq_record)
    for i, jsonpath in enumerate(file_list):
        with open(jsonpath) as jsonfile:
            j = json.load(jsonfile)
        search = j['BlastOutput2']['report']['results']['search']
        try:
            if search["message"] == "No hits found":
                print("Breaked at:", jsonpath)
                continue
        except Exception:
            pass
        brokstuk_header = f">{search['query_title']}"
        query_len = search['query_len']
        for hit in search['hits']:
            if hit['num'] > 1:
                break
                
            alignment_value_list = []
            gene_value_list = []
            NCBI_ID, description = hit['description'][0]['title'].split(' ', 1)
            hsp = hit['hsps'][0]

            # gene tabel data
            gene_value_list.append(NCBI_ID)

            try:
                gene_name = description.split("gene_symbol:")[1].split(" ")[0]
                gene_value_list.append(gene_name)
            except IndexError:
                gene_value_list.append("unknown")
                
            for seq_rec in blast_db:
                if seq_rec.id == NCBI_ID:
                    gene_value_list.append(seq_rec.seq.__str__())

            gene_value_list.append(description)

            gene_data.add(tuple(gene_value_list))

            # alignment tabel data
            alignment_value_list.append(brokstuk_header)
            alignment_value_list.append(hit['num'])
            alignment_value_list.append(NCBI_ID)
            alignment_value_list.append(hsp['align_len'])
            alignment_value_list.append(hsp['evalue'])
            alignment_value_list.append(hsp['bit_score'])
            alignment_value_list.append(round(hsp['identity'] / query_len * 100, 3))
            alignment_value_list.append(hsp['gaps'])
            alignment_value_list.append(hsp['align_len'] - hsp['identity'] - hsp['gaps'])
            alignment_value_list.append(hsp['hit_from'])
            alignment_value_list.append(hsp['hit_to'])
            alignment_data.append(alignment_value_list)
    return alignment_data, gene_data


def tf_main(cursor):
    directory = r'blast_db/blast_json'
    file_list = []
    with open(f"{directory}/blast_results.json") as file:
        j = json.load(file)

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if "blast_results_" in filename:
            file_list.append(f)
    file_list.sort(key= lambda x: int(x.split("_")[-1].split(".")[0]))

    align_data, gene_data = parse_blast(file_list)
    fill_table_brokstuk(cursor)
    fill_table_gene(cursor, gene_data)
    fill_table_alignment(cursor, align_data)
    

if __name__ == "__main__":
    tf_main()
