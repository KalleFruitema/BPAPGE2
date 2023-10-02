import os
import json
from pprint import pprint
from Bio import SeqIO
import requests


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


def fill_table_protein(cursor, data):
    sql = """INSERT INTO PROTEIN
    VALUES(%s, %s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["NCBI_prot_ID"], item["prot_name"], item["prot_sequence"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Protein table filled!")


def fill_table_gene_protein(cursor, data):
    sql = """INSERT INTO GENE_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["ENSEMBL_gene_ID"], item["NCBI_prot_ID"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Gene_protein table filled!")


def fill_table_pathway(cursor, data):
    sql = """INSERT INTO PATHWAY
    VALUES(%s, %s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["pathway_ID"], item["pathway_name"], item["pathway_description"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Pathway table filled!")


def fill_table_pathway_protein(cursor, data):
    sql = """INSERT INTO PATHWAY_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["NCBI_prot_ID"], item["pathway_ID"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Pathway_protein table filled!")


def fill_table_function(cursor, data):
    sql = """INSERT INTO FUNCTION
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["prot_function_ID"], item["prot_function"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Function table filled!")


def fill_table_function_protein(cursor, data, data_ids):
    sql = """INSERT INTO FUNCTION_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        _id = [fn_id["prot_function_ID"] for fn_id in data_ids if fn_id["prot_function"] == item["prot_function"]]
        data_check.add(tuple([item["NCBI_prot_ID"], _id[0]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Function_protein table filled!")


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
                # print("Breaked at:", jsonpath)
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


def togows(gene_data):
    kegg_gene_url = "http://togows.org/entry/kegg-genes/ppad:{}.json"
    json_dict = {}
    for i in gene_data:
        if i[1] == "unknown":
            continue
        gene_req = requests.get(kegg_gene_url.format(i[1])).json()
        if gene_req:
            json_dict.update({
                i[0]: gene_req
            })
    protein_data = []
    for i, y in json_dict.items():
        dict_insert = {
            "ENSEMBL_gene_ID": i,
            "NCBI_prot_ID": y[0]["dblinks"]["NCBI-ProteinID"][0],
            "prot_name": y[0]["name"],
            "prot_sequence": y[0]["aaseq"],
            "pathways": y[0]["pathways"]
        }
        if dict_insert not in protein_data:
            protein_data.append(dict_insert)

    kegg_pathway_url = "http://togows.org/entry/kegg-pathway/{}.json"
    pathway_data = []
    function_data = []
    func_list = set()
    for prot in protein_data:
        for pw_id, pw_name in prot["pathways"].items():
            pw_req = requests.get(kegg_pathway_url.format(pw_id)).json()
            if not any([1 if pw_id in used.values() else 0 for used in pathway_data]):
                pathway_data.append({
                    "NCBI_prot_ID": prot["NCBI_prot_ID"],
                    "pathway_ID": pw_id,
                    "pathway_name": pw_name,
                    "pathway_description": pw_req[0]["description"]
                })
            for func in pw_req[0]["classes"]:
                dict_insert = {
                    "NCBI_prot_ID": prot["NCBI_prot_ID"],
                    "prot_function": func
                }
                func_list.add(func)
                if dict_insert not in function_data:
                    function_data.append(dict_insert)
    function_data_ids = []
    count = 1
    for func in func_list:
        function_data_ids.append({
            "prot_function_ID": f"func_{count}",
            "prot_function": func
        })
        count += 1
    return protein_data, pathway_data, function_data, function_data_ids


def get_table_data():
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
    protein_data, pathway_data, function_data, function_data_ids\
          = togows(gene_data)
    return align_data, gene_data, protein_data, pathway_data, \
        function_data, function_data_ids


def tf_main():
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
    protein_data, pathway_data, function_data, function_data_ids\
          = togows(gene_data)
    pprint(pathway_data)
    print("===="*100)
    pprint(function_data)
    

if __name__ == "__main__":
    tf_main()
