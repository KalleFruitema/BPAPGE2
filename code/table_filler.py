import os
import json
from pprint import pprint
from Bio import Entrez


Entrez.api_key = "MyAPIKey"
Entrez.email = "kallefruitema@gmail.com"


# deze functie werkt helemaal
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


# deze functie werkt, alleen de GENE tabel moet eerst gevuld worden vanwege foreign keys
def fill_table_alignment(cursor, data):
    sql = """INSERT INTO ALIGNMENT(brokstuk_header, alignment_ID, NCBI_gene_ID, 
    alignment_length, e_value, bit_score, percentage_identity, gaps,
    mismatches, startpos_hit, endpos_hit, best_hit_brokstuk)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for line in data:    
        cursor.execute(sql, line)

# ik loop vast op de data hiervan krijgen
def fill_table_gene(cursor, data):
    ...


def parse_blast(file_list):
    # os.popen('sh blast_db/blast_json/blast_script.sh')
    alignment_data = []
    gene_data = []
    for i, jsonpath in enumerate(file_list):
        with open(jsonpath) as jsonfile:
            j = json.load(jsonfile)
        search = j['BlastOutput2']['report']['results']['search']
        brokstuk_header = f">{search['query_title']}"
        query_len = search['query_len']
        for hit in search['hits']:
            alignment_value_list = []
            gene_value_list = []
            NCBI_ID, description = hit['description'][0]['title'].split(' ', 1)
            hsp = hit['hsps'][0]

            # gene tabel data
            gene_value_list.append(NCBI_ID)
            try:
                gene_name = description.split("description:")[1]
                gene_value_list.append(gene_name)
            except IndexError:
                gene_value_list.append("unknown")
            
            try:
                result = Entrez.esearch(db="nucleotide", term=f"{NCBI_ID}")
            except Exception:
                try:
                    term = description.split("gene:")[1].split(" ")[0]
                    result = Entrez.esearch(db="nucleotide", term=f"{term}")
                except Exception:
                    try:
                        term = description.split("transcript:")[1].split(" ")[0]
                        result = Entrez.esearch(db="nucleotide", term=f"{term}")
                    except Exception:
                        result = None
            if result is None:
                gene_value_list.append("unknown")
                # print("Failed")
            else:
                record = Entrez.read(result)["IdList"][0]
                print(record)
            gene_value_list.append(description)

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
            if hit['num'] == 1:
                alignment_value_list.append(True)
            else:
                alignment_value_list.append(False)
            alignment_data.append(alignment_value_list)
            gene_data.append(gene_value_list)
        break
    return alignment_data


def tf_main():
    directory = r'blast_db\blast_json'
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if "blast_results_" in filename:
            file_list.append(f)
    file_list.sort(key= lambda x: int(x.split("_")[-1].split(".")[0]))

    blast_results = parse_blast(file_list)
    # fill_table_brokstuk(cursor)
    # fill_table_alignment(cursor, blast_results)


if __name__ == "__main__":
    tf_main()
